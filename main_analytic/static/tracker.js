(function () {
    'use strict';

    // 1. Initialization Module
    const script = document.currentScript;
    if (!script) return;

    const apiKey = script.getAttribute('data-api-key');
    const siteId = script.getAttribute('data-site-id');
    if (!apiKey) return;

    // Detect API base URL from the script source
    const scriptUrl = new URL(script.src);
    const apiBase = `${scriptUrl.origin}/api`;

    // Prevent double initialization
    if (window.__ANALYTICS_INITIALIZED__) return;
    window.__ANALYTICS_INITIALIZED__ = true;

    // 2. Visitor Management Module
    function generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    function getVisitorId() {
        let visitorId = localStorage.getItem('analytics_visitor_id');
        if (!visitorId) {
            visitorId = generateUUID();
            localStorage.setItem('analytics_visitor_id', visitorId);
        }
        return visitorId;
    }

    const visitorId = getVisitorId();

    // 3. Page & Session Tracking Module
    async function trackPageView() {
        const payload = {
            api_key: apiKey,
            site_id: siteId,
            visitor_id: visitorId,
            page_url: window.location.href,
            referrer: document.referrer || '',
            timestamp: new Date().toISOString()
        };

        try {
            await fetch(`${apiBase}/collect/start/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        } catch (e) {
            // Fail silently
        }
    }

    // 4. Heartbeat Module (Ping)
    function startHeartbeat() {
        const sendPing = async () => {
            const payload = {
                api_key: apiKey,
                site_id: siteId,
                visitor_id: visitorId
            };

            try {
                await fetch(`${apiBase}/collect/ping/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
            } catch (e) {
                // Fail silently
            }
        };

        // Send initial ping immediately
        sendPing();

        // Repeat every 2 minutes (120,000 ms)
        setInterval(sendPing, 120000);
    }



    // 5. Session End Module
    let alreadyEnded = false;
    function endSession() {
        if (alreadyEnded) return;
        alreadyEnded = true;

        const payload = JSON.stringify({
            api_key: apiKey,
            site_id: siteId,
            visitor_id: visitorId
        });

        if (navigator.sendBeacon) {
            // Using a Blob with text/plain avoids CORS preflight (OPTIONS)
            // which is essential for tab-close reliability.
            const blob = new Blob([payload], { type: 'text/plain' });
            navigator.sendBeacon(`${apiBase}/collect/end/`, blob);
        } else {
            // Fallback for very old browsers
            fetch(`${apiBase}/collect/end/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: payload,
                keepalive: true
            }).catch(() => { });
        }
    }

    // 6. Activity Listener (Keep-alive)
    function trackVisibility() {
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'hidden') {
                // We don't necessarily want to ALWAYS end session on hidden (could be just switching tabs)
                // But for many trackers, this is the safest place to ensure THE LAST ping is sent.
                // However, our endSession() explicitly CLOSES the session in the DB.
                // If we want to support switching back, we shouldn't call endSession here.
                // Instead, we just rely on beforeunload for actual closing.
            }
        });
    }

    // SPA Handling (Normal and SPA Apps)
    function initSPA() {
        const originalPushState = history.pushState;
        const originalReplaceState = history.replaceState;

        history.pushState = function () {
            originalPushState.apply(this, arguments);
            trackPageView();
        };

        history.replaceState = function () {
            originalReplaceState.apply(this, arguments);
            trackPageView();
        };

        window.addEventListener('popstate', trackPageView);
    }

    // Hook it all up
    try {
        // Initial page load tracking
        trackPageView();

        // Start heartbeat
        startHeartbeat();

        // Listen for navigation changes (SPA support)
        initSPA();

        // Handle session end
        // 'pagehide' is more reliable than 'unload' for modern browsers
        window.addEventListener('pagehide', (event) => {
            endSession();
        });

        // Fallback for older browsers
        window.addEventListener('beforeunload', () => {
            endSession();
        });

        // Use visibilitychange to catch backgrounding on mobile
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'hidden') {
                // For mobile, hidden often means the app is being closed
                // However, we only want to END the session if the user is actually leaving.
                // sendBeacon handles this well in pagehide.
            }
        });

    } catch (e) {
        // Ultimate silent failure
    }

})();