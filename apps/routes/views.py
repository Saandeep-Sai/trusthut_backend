from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.routes import services


@api_view(['POST'])
def score_routes(request):
    """Score route safety based on nearby TrustHut reports.

    Expects: { routes: [{ polyline, summary, distance, duration }] }
    Returns: routes with risk scores, sorted safest first.
    """
    routes_data = request.data.get('routes', [])

    if not routes_data:
        return Response(
            {'status': 'error', 'message': 'At least one route is required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Fetch all posts once for scoring all routes
    all_posts = services.get_all_posts_for_scoring()

    scored = []
    for i, route in enumerate(routes_data):
        polyline = route.get('polyline', '')
        if not polyline:
            continue

        # Decode polyline → lat/lng points, then sample every 20th point
        points = services.decode_polyline(polyline)
        waypoints = services.sample_waypoints(points, interval=20)

        # Score this route
        score_data = services.score_route(waypoints, all_posts, radius_m=500)

        scored.append({
            'route_index': i,
            'summary': route.get('summary', f'Route {i + 1}'),
            'distance': route.get('distance', ''),
            'duration': route.get('duration', ''),
            'polyline': polyline,
            **score_data,
        })

    # Sort by risk score ascending (safest first)
    scored.sort(key=lambda r: r['risk_score'])

    return Response({'status': 'success', 'data': scored})
