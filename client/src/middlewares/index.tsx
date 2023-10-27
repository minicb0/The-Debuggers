import { Outlet, Navigate } from "react-router-dom";

export const PrivateWrapper = () => {
	if(sessionStorage.getItem("jwt") != null) {
		return <Outlet />;
	}  else {
		return <Navigate to="/" />;
	}
};
