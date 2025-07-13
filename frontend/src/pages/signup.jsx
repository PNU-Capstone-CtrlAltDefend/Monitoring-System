'use client';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, TextField, Button, Typography, Box } from '@mui/material';

const backendUrl = process.env.REACT_APP_API_URL;

const SignUp = () => {
  const [formData, setFormData] = useState({
    manager_id: '',
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    organization_name: '',
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      alert('비밀번호가 일치하지 않습니다.');
      return;
    }

    const payload = { ...formData };
    delete payload.confirmPassword;

    try {
      console.log('회원가입 요청:', backendUrl)
      const response = await fetch(`${backendUrl}/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error(`서버 응답 실패: ${response.status}`);

      const result = await response.json();
      console.log('서버 응답:', result);
      alert('회원 가입이 완료되었습니다.');
      navigate('/'); // 회원가입 후 홈으로 이동

    } catch (error) {
      console.error('회원가입 중 오류 발생:', error);
      alert('회원가입에 실패했습니다.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Container maxWidth="sm" className="py-16">
        <Typography variant="h4" component="h1" align="center" gutterBottom className="font-semibold">
          Sentra 보안 플랫폼 회원가입
        </Typography>

        <Typography variant="body1" align="center" color="textSecondary" className="mb-8">
          회원 가입을 위해 아래 양식을 작성하세요.
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
          <TextField
            label="비밀번호 확인"
            type="password"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
            fullWidth
          />
          <TextField
            label="이름"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            fullWidth
          />
          <TextField
            label="이메일"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            fullWidth
          />
          <TextField
            label="조직명"
            name="organization_name"
            value={formData.organization_name}
            onChange={handleChange}
            required
            fullWidth
          />

          <Button type="submit" variant="contained" color="primary" size="large">
            가입하기
          </Button>
        </Box>
      </Container>
    </div>
  );
}
export default SignUp;  