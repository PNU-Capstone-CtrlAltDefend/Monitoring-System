import React, { useState, useMemo, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
    List,
    ListItemButton,
    ListItemText,
    Collapse,
} from '@mui/material';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';

const VerticalNavbar = ({ isExpanded }) => {
    const navigate = useNavigate();
    const location = useLocation();

    const [statisticsOpen, setStatisticsOpen] = useState(false);

    useEffect(() => {
        if (!isExpanded) setStatisticsOpen(false);
    }, [isExpanded]);

    const handleListItemClick = (path) => {
        navigate(`/${path}`);
    };

    const isActive = useMemo(
        () => (path) => location.pathname === `/${path}`,
        [location.pathname]
    );

    const listItemStyle = {
        '&.Mui-selected': {
            backgroundColor: 'primary.light',
            color: 'text.primary',
            '& .MuiListItemText-primary': {
                color: 'text.primary',
                fontWeight: 600,
            },
        },
        '&:hover': {
            backgroundColor: 'primary.main',
            color: 'text.primary',
        },
        px: 3,
        py: 1.5,
    };

    return (
        <aside
            className={`transition-all duration-300 ease-in-out ${isExpanded ? 'w-64' : 'w-0'
                } overflow-hidden border-r border-gray-700 bg-background.paper`}
        >
            <List dense disablePadding>
                <ListItemButton
                    onClick={() => handleListItemClick('Dashboard')}
                    selected={isActive('Dashboard')}
                    sx={listItemStyle}
                >
                    <ListItemText primary="Dashboard" />
                </ListItemButton>

                <ListItemButton
                    onClick={() => handleListItemClick('Organization Network Topology')}
                    selected={isActive('Organization Network Topology')}
                    sx={listItemStyle}
                >
                    <ListItemText primary="Organization Network Topology" />
                </ListItemButton>

                <ListItemButton
                    onClick={() => handleListItemClick('AssetInformation')}
                    selected={isActive('AssetInformation')}
                    sx={listItemStyle}
                >
                    <ListItemText primary="Asset Information" />
                </ListItemButton>

                <ListItemButton
                    onClick={() => handleListItemClick('RiskAssessment')}
                    selected={isActive('RiskAssessment')}
                    sx={listItemStyle}
                >
                    <ListItemText primary="Risk Assessment" />
                </ListItemButton>

                <ListItemButton
                    onClick={() => handleListItemClick('report')}
                    selected={isActive('report')}
                    sx={listItemStyle}
                >
                    <ListItemText primary="Report" />
                </ListItemButton>
            </List>
        </aside>
    );
};

export default VerticalNavbar;