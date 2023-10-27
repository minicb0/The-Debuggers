import { serverURL } from "../../config";

export const dataFetch = async (
	url: string,
	method: "POST",
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	body: any = JSON.stringify({})
) => {
	const headers = {
		"Content-Type": "application/json",
		Authorization: `Bearer ${sessionStorage.getItem("jwt")}`,
	};
	const response = await fetch(`${serverURL}${url}`, {
		method,
		headers,
		body: body,
	});
	return response;
};