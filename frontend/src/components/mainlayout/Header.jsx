import theme from '../../themes.jsx';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Header = () => {
    const navigate = useNavigate();
    const handleLoginClick = () => {
        navigate('/signin');
    };
    return (
        <AppBar position="static" color="default" elevation={1}>
            <Toolbar className="flex justify-between">
                <Typography variant="h5" color='#e4e4e7' className="font-bold">
                    Sentra
                </Typography>
                <Box className="space-x-4">
                    <Button color="inherit">기능</Button>
                    <Button color="inherit">지원</Button>
                    <Button color="inherit" onClick={handleLoginClick}>로그인</Button>
                </Box>
            </Toolbar>
        </AppBar>
    );
};

export default Header;
