class Paycom {
    constructor(form, button) {
        var i = this.e(form, "Форма не найдена"),
            u = this.e(button, "Контейнер кнопки не найден"),
            l = this.t(i),
            d = {
                l: l.lang,
                m: l.merchant,
                a: l.amount,
                ac: l.account,
                c: l.callback,
                ct: l.callback_timeout,
            },
            m = this.o(d),
            s = this.n(m);
        i.addEventListener("submit", function (e) {
            e.preventDefault();
            console.log(s);
            var t = l.endpoint + s;
            return document.location = t, !1
        }),
            this.a(u, l);

    }

    QR = {
        isSupport: !!window.WebSocket || window.MozWebSocket
    }
    e(e, t) {
        var n;
        return (
            "function" == typeof jQuery && e instanceof jQuery && (n = e[0]),
            e instanceof HTMLElement && (n = e),
            "string" == typeof e && (n = document.querySelector(e)),
            n ? n : console.error(t)
        );
    }
    t(e) {
        var t = {};
        if (!e.getAttribute("action"))
            return console.error("Неверный URL формы");
        if (
            ((t.endpoint = e.getAttribute("action")),
                (t.merchant = e.querySelector("[name=merchant]").value),
                !t.merchant || !/^[a-f\d]{24}$/i.test(t.merchant))
        )
            return console.error("Неверный идентификатор поставщика");
        if (((t.amount = +e.querySelector("[name=amount]").value), !t.amount))
            return console.error("Неверная сумма");
        t.account = {};
        for (var n = e.children, o = 0; o < n.length; ++o) {
            var r = n[o];
            if (/^account\[.+\]$/.test(r.name)) {
                var a = r.name.substring(8, r.name.indexOf("]", 8));
                t.account[a] = r.value;
            }
        }
        if (0 === Object.keys(t.account).length)
            return console.error("Неверный аккаунт");
        if (
            ((t.description = e.querySelector("[name=description]") ?
                e.querySelector("[name=description]").value :
                void 0),
                (t.detail = e.querySelector("[name=detail]") ?
                    e.querySelector("[name=detail]").value :
                    void 0),
                (t.lang = e.querySelector("[name=lang]") ?
                    e.querySelector("[name=lang]").value :
                    "ru"),
                (t.button = "colored"),
                e.querySelector("[name=button]"))
        ) {
            var c = e.querySelector("[name=button]");
            (t.button = c.value),
                (t.button_width = c.dataset.width || 0),
                (t.button_height = c.dataset.height || 0),
                (t.button_type = c.dataset.type || "svg");
        }
        if (e.querySelector("[name=qr]")) {
            var i = e.querySelector("[name=qr]");
            (t.qr = i.value),
                (t.qr_width = i.dataset.width),
                (t.qr_height = i.dataset.height);
        }
        return (
            (t.callback = e.querySelector("[name=callback]") ?
                e.querySelector("[name=callback]").value :
                void 0),
            (t.callback_timeout = e.querySelector("[name=callback_timeout]") ?
                e.querySelector("[name=callback_timeout]").value :
                void 0),
            t
        );
    }
    n(e) {
        return btoa(
            encodeURIComponent(e).replace(/%([0-9A-F]{2})/g, function (e, t) {
                return String.fromCharCode("0x" + t);
            })
        );
    }
    o(e) {
        var t = "";
        return (
            Object.keys(e).forEach(function (n) {
                e[n] &&
                    ("ac" == n && "object" == typeof e[n] ?
                        Object.keys(e[n]).forEach(function (o) {
                            e[n][o] &&
                                (t += (t ? ";" : "") + n + "." + o + "=" + e[n][o]);
                        }) :
                        (t += (t ? ";" : "") + n + "=" + e[n]));
            }),
            t
        );
    }
    r(e) { for (; e.firstChild;) e.removeChild(e.firstChild); }
    a(e, t) {
        this.r(e);
        var n = document.createElement("input");
        n.setAttribute("type", "image"),
            (n.src =
                "https://cdn.paycom.uz/integration/images/btn_" +
                t.button +
                "_" +
                t.lang +
                "." +
                t.button_type),
            t.button_width && n.setAttribute("width", t.button_width),
            t.button_height && n.setAttribute("height", t.button_height),
            e.appendChild(n);
    }
}