<picture>
  <source media="(max-width: 640px) and (prefers-color-scheme: dark)" srcset="./assets/zirtuno-liquid-dark-mobile.svg?v=20260928">
  <source media="(max-width: 640px)" srcset="./assets/zirtuno-liquid-light-mobile.svg?v=20260928">
  <source media="(prefers-color-scheme: dark)" srcset="./assets/zirtuno-liquid-dark.svg?v=20260928">
  <source media="(prefers-color-scheme: light)" srcset="./assets/zirtuno-liquid-light.svg?v=20260928">
  <img alt="Pedro Mautone — Co-Founder &amp; Systems Architect at Zirtuno. Animated liquid console; dated contribution data is linked below." src="./assets/zirtuno-liquid-dark.svg?v=20260928" width="100%">
</picture>

<div align="center">

**[Zirtuno](https://github.com/ZIRTUNO)** · **[zirtuno.com ↗](https://zirtuno.com)** · **[LinkedIn](https://www.linkedin.com/in/pedro-mautone/)** · **[pedropaivamautone@gmail.com](mailto:pedropaivamautone@gmail.com)**

</div>

---

### Systems Architecture & Engineering

#### [Zirtuno Systems Core](https://github.com/ZIRTUNO)
`Next.js` `TypeScript` `WebGL2` `Raw GLSL` `PostgreSQL` `Redis` `Docker`
- Co-founded Zirtuno, engineering connected software, real-time 3D pipelines, and high-concurrency cloud backends.
- Architected the R5 fluid engine and persistent WebGL2 chapter canvas, coordinating metaball dynamics, spatial tile-binning, and scroll-driven transitions.
- Engineered resilient API gateways and automated event-driven sync microservices powering client ecosystems.

#### [Direction-Aware Smart Parking & Edge Vision Telemetry](https://github.com/Pedrowtst/smart-parking-esp32)
`C++` `ESP32-CAM` `YOLOv8` `BoT-SORT` `Python` `Flask` `OpenCV`
- Built an ESP32-CAM video pipeline with MJPEG streaming over Wi-Fi and Python-based detection and tracking on a laptop.
- Turned directional line crossings into vehicle entry, exit, occupancy, and available-space counts in a real-time Flask dashboard.
- Added camera discovery, reconnection, and configurable counting behavior. Developed as an academic prototype for a trusted local network.

[Source & setup →](https://github.com/Pedrowtst/smart-parking-esp32) · [Documentação em português →](https://github.com/Pedrowtst/smart-parking-esp32/blob/main/LEIAME.md)

#### Enterprise ERP / CRM Bi-directional Data Bus
`Python` `FastAPI` `PostgreSQL` `Redis` `Docker` `Nginx`
- High-throughput bi-directional data synchronization pipeline connecting legacy on-premise ERP databases with modern cloud CRM endpoints.
- Applied transactional outbox patterns, exponential backoff retries, and idempotent workers to keep synchronization recoverable.
- Connected event flows and health checks across disparate schemas, with explicit handling for retries and failures.

#### Low-Level Protocol Engineering & Reverse Engineering
`C` `C++` `Linux / POSIX` `GDB` `Sockets` `Binary Analysis`
- Static and dynamic reverse engineering of proprietary binary communication protocols.
- Packet inspection, low-level socket programming, and automated payload parsing utilities for legacy industrial hardware bridges.
- Memory profiling and deterministic execution analysis under strict POSIX timing constraints.

---

### Engineering Principles & Architectural Invariants

- **Predictable Latency**: Define timing budgets, measure behavior, and keep slow paths visible before optimizing throughput.
- **Transactional Idempotency & Fault Isolation**: Data integrity is preserved across network partitions using transactional outbox structures, deterministic deduplication, and atomic persistence.
- **Continuous Liquid Continuity**: High-performance graphical pipelines run on single persistent contexts, tile-binned spatial partitioning, and strict frame pacing.

---

### Technical Matrix

| Domain | Technologies & Practices |
| :--- | :--- |
| **Low-Level & Embedded** | C, C++, FreeRTOS, ESP32-CAM, Linux / POSIX Internals, GDB, Socket Programming, Reverse Engineering |
| **Distributed Backends** | Python, FastAPI, Flask, PostgreSQL, Redis, REST APIs, WebSockets, SQLAlchemy, Transactional Outbox |
| **Enterprise & Infrastructure** | Docker, Nginx, ERP/CRM Synchronization Engines, Microservices Architecture, CI/CD, Bash |
| **Edge Computer Vision** | YOLOv8, BoT-SORT, OpenCV, MJPEG Streaming, Direction-Aware Vehicle Tracking |

---

<div align="center">
<sub>One continuous liquid. Original Zirtuno identity, with a daily GitHub contribution snapshot. The current month is partial; motion is decorative.</sub>
</div>

<details>
<summary>About the numbers</summary>

Commits and contributions cover the dated period shown in the header. Public projects and language percentages cover owned, public, non-fork, non-archived repositories, excluding this profile. The language mix reflects code bytes, not proficiency or all work at Zirtuno.

[Dated source data](./cache/data.json) · [Update workflow](https://github.com/Pedrowtst/Pedrowtst/actions/workflows/update-readme.yml) · [Maintenance notes](./docs/PROFILE.md)

</details>
