// function e(e, t) {
//     var n;
//     return "function" == typeof jQuery && e instanceof jQuery && (n = e[0]),
//         e instanceof HTMLElement && (n = e),
//         "string" == typeof e && (n = document.querySelector(e)),
//         n ? n : console.error(t)
// }

// function t(e) {
//     var t = {};
//     if (!e.getAttribute("action")) return console.error("Неверный URL формы");
//     if (
//         t.endpoint = e.getAttribute("action"),
//         t.merchant = e.querySelector("[name=merchant]").value,
//         !t.merchant || !/^[a-f\d]{24}$/i.test(t.merchant)) return console.error("Неверный идентификатор поставщика");
//     if (t.amount = +e.querySelector("[name=amount]").value, !t.amount) return console.error("Неверная сумма");
//     t.account = {};
//     for (var n = e.children, o = 0; o < n.length; ++o) {
//         var r = n[o];
//         if (/^account\[.+\]$/.test(r.name)) {
//             var a = r.name.substring(8, r.name.indexOf("]", 8));
//             t.account[a] = r.value
//         }
//     }
//     if (0 === Object.keys(t.account).length) return console.error("Неверный аккаунт");
//     if (
//         t.description = e.querySelector("[name=description]") ? e.querySelector("[name=description]").value : void 0,
//         t.detail = e.querySelector("[name=detail]") ? e.querySelector("[name=detail]").value : void 0,
//         t.lang = e.querySelector("[name=lang]") ? e.querySelector("[name=lang]").value : "ru",
//         t.button = "colored", e.querySelector("[name=button]")) {
//         var c = e.querySelector("[name=button]");
//         t.button = c.value,
//             t.button_width = c.dataset.width || 0, t.button_height = c.dataset.height || 0, t.button_type = c.dataset.type || "svg"
//     }
//     if (e.querySelector("[name=qr]")) {
//         var i = e.querySelector("[name=qr]");
//         t.qr = i.value,
//             t.qr_width = i.dataset.width,
//             t.qr_height = i.dataset.height
//     }
//     return t.callback = e.querySelector("[name=callback]") ? e.querySelector("[name=callback]").value : void 0,
//         t.callback_timeout = e.querySelector("[name=callback_timeout]") ? e.querySelector("[name=callback_timeout]").value : void 0, t
// }

// function n(e) {
//     return btoa(encodeURIComponent(e).replace(/%([0-9A-F]{2})/g, function (e, t) {
//         return String.fromCharCode("0x" + t)
//     }))
// }

// function o(e) {
//     var t = "";
//     return Object.keys(e).forEach(function (n) {
//         e[n] && ("ac" == n && "object" == typeof e[n] ? Object.keys(e[n]).forEach(function (o) {
//             e[n][o] && (t += (t ? ";" : "") + n + "." + o + "=" + e[n][o])
//         }) : t += (t ? ";" : "") + n + "=" + e[n])
//     }), t
// }

// function r(e) {
//     for (; e.firstChild;) e.removeChild(e.firstChild)
// }

// function a(e, t) {
//     r(e);
//     var n = document.createElement("input");
//     n.setAttribute("type", "image"), n.src = "https://cdn.paycom.uz/integration/images/btn_" + t.button + "_" + t.lang + "." + t.button_type, t.button_width && n.setAttribute("width", t.button_width), t.button_height && n.setAttribute("height", t.button_height), e.appendChild(n)
// }

// function c(e, t) {
//     r(t.qrBlock);
//     var n = new i(t.endpoint.replace(/^http/, "ws")),
//         o = document.createElement("img");
//     t.qr_width && o.setAttribute("width", t.qr_width), t.qr_height && o.setAttribute("height", t.qr_height), n.onmessage = function (e) {
//         o.src = e.data, t.qrBlock.appendChild(o)
//     }, n.onclose = function (n) {
//         if (4010 === n.code) {
//             if (t.onSuccess) return t.onSuccess();
//             t.callback ? window.location.href === t.callback ? location.reload() : window.location.href = t.callback : location.reload()
//         }
//         if (4011 === n.code) {
//             if (t.onError) return t.onError();
//             location.reload()
//         }
//         4e3 === n.code && (console.error(n.code, n.reason), t.onError && t.onError()), 1006 === n.code && setTimeout(c(e, t), 2e3), t.qrBlock.removeChild(o)
//     }, n.onopen = function () {
//         n.send(JSON.stringify(e))
//     }
// }
// window.Paycom || (window.Paycom = {});
// var i = window.WebSocket || window.MozWebSocket;
// Paycom.QR = function (n, o, r, a) {
//     if (!i) return console.error("Отсутствует поддержка WebSocket");
//     var u = e(n, "Форма не найдена"),
//         l = e(o, "Блок QR не найден"),
//         d = t(u);
//     d.qrBlock = l, d.onSuccess = r, d.onError = a;
//     var m = {
//         lang: d.lang,
//         merchant: d.merchant,
//         amount: d.amount,
//         account: d.account,
//         description: d.description,
//         detail: d.detail
//     };
//     c(m, d)
// }, Paycom.QR.isSupport = !!i, Paycom.Button = function (form, button) {
//     var i = e(form, "Форма не найдена"),
//         u = e(button, "Контейнер кнопки не найден"),
//         l = t(i),
//         d = {
//             l: l.lang,
//             m: l.merchant,
//             a: l.amount,
//             ac: l.account,
//             c: l.callback,
//             ct: l.callback_timeout
//         },
//         m = o(d),
//         s = n(m);
//     i.addEventListener("submit", function (e) {
//         alert("dfgdfgfdg");
//         e.preventDefault();
//         console.log(l);
//         var t = l.endpoint + s;
//         // return document.location = t, !1
//     }), a(u, l)
// }
























