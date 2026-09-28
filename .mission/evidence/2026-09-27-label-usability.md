# Evidence — Label margin and mobile clearing, 2026-09-27

The owner reported that the first printed line was clipped and repeated mobile entry needed faster clearing. The API now offsets the top rule and all content by 24 dots at 203 dpi (about 3 mm), with matching SVG preview coordinates. The UI has a 44 px clear button for each populated field and a Clear fields action that keeps template and copy count.

Validation: six API unit tests passed, including 203 and 300 dpi ZPL coordinates and SVG offset; `npm --prefix web run build` passed; `git diff --check` passed. Builderx published `zelabel-api:2.0.1` at `sha256:19d0310e449528884896c6d4814a08420b4eff4b694f63554aefa30d57d6c8f2` and `zelabel-ui:2.0.1` at `sha256:f62027385749784c55ca19cf2b8fbd74c0c390802858d7913224a746500826bc`.

The vnme server dry run passed. Applying `k8s/zelabel.yaml` rolled out a new 3/3 Ready pod with both expected image IDs and `LABEL_TOP_OFFSET_DOTS=24`. A live API preview included the expected shifted rule and text coordinates. The deployed UI asset contained `Clear fields`. An unauthenticated HTTPS request to `https://labels.vanness.life/` returned a 302 to Pocket ID. The operations manifest in `k3s-three/zlabel` matches the application manifest. No physical print was sent during validation; paper alignment needs an owner check.
