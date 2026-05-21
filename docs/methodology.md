# Methodology

This showcase uses deterministic synthetic data to mirror a MATLAB-style communication-network simulation pipeline.

## Model

- A 19-cell hexagonal layout is generated in axial coordinates.
- Inter-cell coupling decays with distance and is normalized to a compact interference index.
- User counts are sampled with a Poisson process.
- Small-scale fading uses a Rayleigh distribution.
- SNR sweeps are evaluated across multiple frequency-reuse and allocation strategies.

## Strategies

- `IFR3`: conservative reuse baseline with reduced spectrum reuse and lower interference.
- `SWF`: synthetic water-filling-inspired allocation with stronger capacity at usable SNR.
- `FFR+IFR3`: edge-focused FFR variant with improved edge SINR.
- `FFR+SWF`: FFR plus SWF-style allocation, combining edge mitigation and capacity gain.

## Validation Philosophy

The checks are qualitative rather than numeric reproduction claims. They verify trends expected from the public project description:

- higher SNR should increase capacity;
- FFR should improve edge-user SINR;
- denser users should increase interference pressure;
- SWF-style allocation should improve total capacity.
