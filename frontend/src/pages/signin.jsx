'use client';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  TextField,
  Button,
  Typography,
  Box,
} from '@mui/material';

const backendUrl = process.env.REACT_APP_API_URL;

const SignIn = () => {
  const [formData, setFormData] = useState({
    manager_id: '',
    password: '',
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      console.log('로그인 요청:', backendUrl);
      const response = await fetch(`${backendUrl}/auth/signin`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error(`서버 응답 실패: ${response.status}`);

      const result = await response.json();
      console.log('서버 응답:', result);

      // 예: 토큰 저장 및 리디렉션
      localStorage.setItem('token', result.token);
      alert('로그인 성공!');
      navigate('/'); // 로그인 후 홈으로 이동

    } catch (error) {
      console.error('로그인 중 오류 발생:', error);
      alert('로그인에 실패했습니다.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Container maxWidth="sm" className="py-16">
        <Typography variant="h4" component="h1" align="center" gutterBottom className="font-semibold">
          Sentra 보안 플랫폼 로그인
        </Typography>

        <Typography variant="body1" align="center" color="textSecondary" className="mb-8">
          계정 정보를 입력하여 로그인하세요.
        </Typography>

        <Box component="form" onSubmit={handleSubmit} className="flex flex-col gap-4">
          <TextField
            label="ID"
            name="manager_id"
            value={formData.manager_id}
            onChange={handleChange}
            required
            fullWidth
          />
          <TextField
            label="비밀번호"
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            fullWidth
          />

          <Button type="submit" variant="contained" color="primary" size="large">
            로그인
          </Button>
        </Box>
      </Container>
    </div>
  );
};

export default SignIn;
