const API_URL = process.env.REACT_APP_API_URL;

export async function signIn({ manager_id, password }) {
  const form = new FormData();
  form.append('username', manager_id);
  form.append('password', password);

  const response = await fetch(`${API_URL}/auth/signin`, {
    method: 'POST',
    body: form, 
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData?.detail || '로그인 실패');
  }

  return await response.json();
}