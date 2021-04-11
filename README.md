# voyapt
Voyage Analysis & Prediction Toolbox - Primarily aimed at the nautical field

High-level concepts:
* `Waypoints` are 2D positions in space. In `voyapt`, a `Waypoint` is an alias for `nvector.GeoPoint`.
* A `Leg` is the path between two `Waypoint`s. In `voyapt`, a `Leg` is an alias for `nvector.GeoPath`.
* A `Route` is a collection of minimum two `Waypoint`s. `Leg`s may be extracted from a `Route`.

### Installation

So far:
* Clone repo
* Run `pip install path/to/repo/root`

### Examples

See `examples/` and `tests/`

