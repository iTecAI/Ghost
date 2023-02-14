export type ApiResponse<T> =
    | {
          success: true;
          data: T;
      }
    | {
          success: false;
          statusCode: number;
          errorCode: string;
          errorText: string;
      };

export async function request<T>(
    method: "get" | "post" | "put" | "delete",
    path: string,
    options?: { params?: { [key: string]: any }; data?: any }
): Promise<ApiResponse<T>> {
    const params =
        options && options.params
            ? "?" + new URLSearchParams(options.params).toString()
            : "";
    const auth: string | null = window.localStorage.getItem("auth");
    const result = await fetch(`/api${path}${params}`, {
        method: method.toUpperCase(),
        headers: auth ? { Authorization: auth } : undefined,
        body:
            (method === "post" || method === "put") && options && options.data
                ? JSON.stringify(options.data)
                : undefined,
    });

    let data: T = (await result.text()) as T;
    try {
        data = JSON.parse(data as string);
    } catch {}

    if (result.status < 400) {
        return { success: true, data };
    } else {
        return {
            success: false,
            statusCode: result.status,
            errorCode: (data as any).errorCode ?? "error.generic",
            errorText: (data as any).detail ?? "An unknown error occurred.",
        };
    }
}

export async function get<T>(
    path: string,
    options?: { params?: { [key: string]: any } }
): Promise<ApiResponse<T>> {
    return await request<T>("get", path, options);
}

export async function del<T>(
    path: string,
    options?: { params?: { [key: string]: any } }
): Promise<ApiResponse<T>> {
    return await request<T>("delete", path, options);
}

export async function put<T>(
    path: string,
    options?: { params?: { [key: string]: any }; data?: { [key: string]: any } }
): Promise<ApiResponse<T>> {
    return await request<T>("put", path, options);
}

export async function post<T>(
    path: string,
    options?: { params?: { [key: string]: any }; data?: { [key: string]: any } }
): Promise<ApiResponse<T>> {
    return await request<T>("post", path, options);
}
