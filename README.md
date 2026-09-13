<picture>
  <source media="(prefers-color-scheme: dark)"  srcset="https://raw.githubusercontent.com/Pedrowtst/Pedrowtst/main/assets/zirtuno-liquid-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Pedrowtst/Pedrowtst/main/assets/zirtuno-liquid-light.svg">
  <img alt="Pedro Mautone — Co-Founder &amp; Systems Architect at Zirtuno" src="https://raw.githubusercontent.com/Pedrowtst/Pedrowtst/main/assets/zirtuno-liquid-dark.svg" width="100%">
</picture>

<div align="center">

**[Zirtuno](https://github.com/ZIRTUNO)** · **[zirtuno.com ↗](https://zirtuno.com)** · **[LinkedIn](https://www.linkedin.com/in/pedro-mautone/)** · **[pedropaivamautone@gmail.com](mailto:pedropaivamautone@gmail.com)**

</div>

---

### Systems Architecture & Engineering

#### [Zirtuno Systems Core](https://github.com/ZIRTUNO)
`Next.js` `TypeScript` `WebGL2` `Raw GLSL` `PostgreSQL` `Redis` `Docker`
- Co-founded Zirtuno, engineering connected software, real-time 3D pipelines, and high-concurrency cloud backends.
- Architected the R5 unified fluid engine and persistent WebGL2 canvas pipeline, handling continuous metaball dynamics, spatial tile-binning, and zero-stutter frame budgets.
- Engineered resilient API gateways and automated event-driven sync microservices powering client ecosystems.

#### [Direction-Aware Smart Parking & Edge Vision Telemetry](https://github.com/Pedrowtst/smart-parking-esp32)
`C++` `ESP32-CAM` `YOLOv8` `BoT-SORT` `Python` `Flask` `FreeRTOS`
- Distributed multi-camera edge vision telemetry system deployed on embedded microcontrollers for intelligent spatial tracking.
- Implemented real-time bi-directional vehicle transit tracking with sub-100ms occupancy event streaming to centralized telemetry servers.
- Built zero-copy frame ingestion pipelines over RTSP with hardware-accelerated inferencing and fault-tolerant reconnection logic.

#### Enterprise ERP / CRM Bi-directional Data Bus
`Python` `FastAPI` `PostgreSQL` `Redis` `Docker` `Nginx`
- High-throughput bi-directional data synchronization pipeline connecting legacy on-premise ERP databases with modern cloud CRM endpoints.
- Implemented transactional outbox patterns, exponential backoff retries, and idempotent distributed message workers handling thousands of transactions daily with zero data loss.
- Engineered real-time event streaming and health checks with sub-second change propagation across disparate schemas.

#### Low-Level Protocol Engineering & Reverse Engineering
`C` `C++` `Linux / POSIX` `GDB` `Sockets` `Binary Analysis`
- Static and dynamic reverse engineering of proprietary binary communication protocols.
- Packet inspection, low-level socket programming, and automated payload parsing utilities for legacy industrial hardware bridges.
- Memory profiling and deterministic execution analysis under strict POSIX timing constraints.

---

### Engineering Principles & Architectural Invariants

- **Predictable Latency over Unbounded Throughput**: Systems are architected with strict timing budgets (<100ms on edge telemetry, <20ms on distributed bus handoffs).
- **Transactional Idempotency & Fault Isolation**: Data integrity is preserved across network partitions using transactional outbox structures, deterministic deduplication, and atomic persistence.
- **Continuous Liquid Continuity**: High-performance graphical pipelines run on single persistent contexts, tile-binned spatial partitioning, and strict frame pacing.

---

### Technical Matrix

| Domain | Production Technologies |
| :--- | :--- |
| **Low-Level & Embedded** | C, C++, FreeRTOS, ESP32-CAM, Linux / POSIX Internals, GDB, Socket Programming, Reverse Engineering |
| **Distributed Backends** | Python, FastAPI, Flask, PostgreSQL, Redis, REST APIs, WebSockets, SQLAlchemy, Transactional Outbox |
| **Enterprise & Infrastructure** | Docker, Nginx, ERP/CRM Synchronization Engines, Microservices Architecture, CI/CD, Bash |
| **Edge Computer Vision** | YOLOv8, BoT-SORT, RTSP Telemetry Streaming, Multi-Camera Spatial Tracking |

---

<div align="center">
<sub>The header organ is a continuous fluid SVG driven by live telemetry from the GitHub GraphQL API, updated daily via automated workflow. Built with authentic Zirtuno R5 liquid identity.</sub>
</div>
