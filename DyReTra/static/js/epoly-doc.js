/*********************************************************************\
    *                                                                     *
    * epolys.js                                          by Mike Williams *
    * updated to API v3                                  by Larry Ross    *
    *                                                                     *
    * A Google Maps API Extension                                         *
    *                                                                     *
    * Adds various Methods to google.maps.Polygon and google.maps.Polyline *
    *                                                                     *
    * .Contains(latlng) returns true is the poly contains the specified   *
    *                   GLatLng                                           *
    *                                                                     *
    * .Area()           returns the approximate area of a poly that is    *
    *                   not self-intersecting                             *
    *                                                                     *
    * .Distance()       returns the length of the poly path               *
    *                                                                     *
    * .Bounds()         returns a GLatLngBounds that bounds the poly      *
    *                                                                     *
    * .GetPointAtDistance() returns a GLatLng at the specified distance   *
    *                   along the path.                                   *
    *                   The distance is specified in metres               *
    *                   Reurns null if the path is shorter than that      *
    *                                                                     *
    * .GetPointsAtDistance() returns an array of GLatLngs at the          *
    *                   specified interval along the path.                *
    *                   The distance is specified in metres               *
    *                                                                     *
    * .GetIndexAtDistance() returns the vertex number at the specified    *
    *                   distance along the path.                          *
    *                   The distance is specified in metres               *
    *                   Returns null if the path is shorter than that      *
    *                                                                     *
    * .Bearing(v1?,v2?) returns the bearing between two vertices          *
    *                   if v1 is null, returns bearing from first to last *
    *                   if v2 is null, returns bearing from v1 to next    *
    *                                                                     *
    *                                                                     *
    ***********************************************************************
    *                                                                     *
    *   This Javascript is provided by Mike Williams                      *
    *   Blackpool Community Church Javascript Team                        *
    *   http://www.blackpoolchurch.org/                                   *
    *   http://econym.org.uk/gmap/                                        *
    *                                                                     *
    *   This work is licenced under a Creative Commons Licence            *
    *   http://creativecommons.org/licenses/by/2.0/uk/                    *
    *                                                                     *
    ***********************************************************************
    *                                                                     *
    * Version 1.1       6-Jun-2007                                        *
    * Version 1.2       1-Jul-2007 - fix: Bounds was omitting vertex zero *
    *                                add: Bearing                         *
    * Version 1.3       28-Nov-2008  add: GetPointsAtDistance()           *
    * Version 1.4       12-Jan-2009  fix: GetPointsAtDistance()           *
    * Version 3.0       11-Aug-2010  update to v3                         *
    *                                                                     *
    \*********************************************************************/
