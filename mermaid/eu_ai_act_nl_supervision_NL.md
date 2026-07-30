---
title: EU AI Act — Nederlands toezichtskader
description: >
  Organisatie van het Nederlandse toezicht onder de EU AI Act. De EU-AI-raad
  coördineert de AP (verboden AI, transparantie, hoog-risico-systemen), de
  RDI (productcoördinatie) en de sectorale toezichthouders (AFM, DNB, etc.).
---
```mermaid
flowchart TB

    EAB["EU-AI-raad"]

    AP[""<b class='hl'>AP</b><br/>Verboden AI<br/>Hoog Risico<br/>Transparantie"]

    RDI["<b class='hl'>RDI</b><br/>Coördinatie<br/>Producten"]

    Sector["<b class='hl'>Sectorale toezichthouders</b><br/>AFM • DNB • NLA • IGJ • ILT • NVWA"]

    EAB --> AP
    EAB --> RDI

    AP <--> RDI

    AP --> Sector
    RDI --> Sector
```
