# Methodology

This showcase uses deterministic synthetic data to mirror the structure of a private MATLAB reproduction pipeline for 5G fractional frequency reuse experiments.

## Model

- A 19-cell hexagonal layout is generated in axial coordinates.
- Inter-cell coupling decays with distance and is normalized to a compact interference index.
- User counts are sampled with a Poisson process.
- Small-scale fading uses a Rayleigh distribution.
- SNR sweeps are evaluated across multiple frequency-reuse and allocation strategies.

## Strategies

- `IFR3`: conservative reuse baseline with reduced spectrum reuse and lower interference.
- `SWF`: synthetic water-filling-inspired allocation with stronger capacity at usable SNR.
- `FFR+IFR3`: edge-focused FFR variant for checking edge SINR gain under fixed equal-power allocation.
- `FFR+SWF`: FFR plus SWF-style allocation, used to check whether edge SINR remains close to SWF under hard spectral isolation.

## Private Reproduction Framing

The related paper is a first-author review in CSIC 2024 / HSET Vol. 124. The private MATLAB project independently reproduced a 19-cell experiment pattern discussed in the reviewed literature. This public repository is a synthetic Python showcase of that reproduction workflow rather than a release of the private MATLAB source or original reproduction outputs.

Verified private MATLAB outputs from 2026-07:

| Check | Result |
| --- | --- |
| Trend configuration | `Nf=12`, `Nsim=3`, `SNR=[0,10,20] dB`, `Um=[6,18]` |
| Capacity gain from 0 to 20 dB | SWF +110.5, FFR+IFR3 +39.6, FFR+SWF +28.2, IFR3 +25.2 bps/Hz |
| FFR+IFR3 vs IFR3 edge SINR | +13% (0.01061 vs 0.009363) |
| FFR+SWF vs SWF edge SINR | About 91% of SWF (0.1076 vs 0.1184) |

## Validation Philosophy

The checks are qualitative rather than numeric reproduction claims. They verify trends expected from the public project description:

- higher SNR should increase capacity;
- FFR should improve edge-user SINR under fixed equal-power allocation;
- FFR+SWF should keep edge-user SINR close to SWF under hard spectral isolation;
- denser users should increase interference pressure;
- SWF-style allocation should improve total capacity.
