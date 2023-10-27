import {
	Home
} from "../pages";

export const publicRoutes: RouteType[] = [
	{
		title: "Home Page",
		path: "/",
		element: <Home />,
	}
];

export const privateRoutes: RouteType[] = [];