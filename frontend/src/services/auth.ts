export const checkLogin = async (email: string, password: string) => {
    const response = await fetch('http://localhost:8000/api/auth/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || 'Login failed');
    }

    return data;
};

export const signup = async (email: string, password: string) => {
    const response = await fetch('http://localhost:8000/api/auth/signup/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || 'Signup failed');
    }

    return data;
};