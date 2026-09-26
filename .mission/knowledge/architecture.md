# ZeLabel v2 architecture

```text
labels.vanness.life → Traefik → Service:4180 → oauth2-proxy (Pocket ID)
                                              ↓ pod loopback
                                       Nginx UI :8080
                                              ↓ /api on loopback
                                       Flask API :8001 → ZD621:9100
```

The API and UI are separate containers in one pod. Nginx routes `/api/` to Flask, avoiding another host. Only oauth2-proxy has a Service port. No persistent application state is stored. Templates are static code and the print job is sent immediately. Preview uses local SVG generated from the same layout coordinates as ZPL. API print POSTs also check the browser Origin.

The UI targets narrow iPhone viewports and shares Pocket ID's quiet visual approach without copying its assets. Pocket ID owns user access; the app has no group or local user checks and does not consume OIDC identity claims. The owner confirmed 203 dpi. Physical stock switching remains an operational step.
