export async function get(apiBase: string, endpoint: string): Promise<any> {
    let fullRequestPath = `${apiBase}${endpoint}`;
    const response = await fetch(fullRequestPath);
    if (!response.ok) {
        throw new Error('')
    }

    return await response.json();
}

export async function post(apiBase: string, endpoint: string, body: string): Promise<any> {
    let fullRequestPath = `${apiBase}${endpoint}`;
    const response = await fetch(fullRequestPath, {
        method: 'POST',
        body
    });
    if (!response.ok) {
        throw new Error('')
    }

    return await response.json();
}
