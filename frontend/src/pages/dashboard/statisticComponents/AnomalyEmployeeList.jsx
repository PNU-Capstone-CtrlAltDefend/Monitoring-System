import React, { useEffect, useState } from 'react';
import { Box, Table, TableBody, TableCell, TableHead, TableRow, CircularProgress } from '@mui/material';
import CommonCard from '../../../components/common/card/CommonCard';
import { fetchAnomalyEmployees } from '../../../services/AnomalyDetection';
import { useParams } from 'react-router-dom';

const AnomalyEmployeeList = () => {
  const { oid } = useParams();
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEmployees = async () => {
      try {
        const data = await fetchAnomalyEmployees(oid);
        setEmployees(data);
      } catch (error) {
        console.error('이상 사용자 목록 데이터를 가져오는 데 실패했습니다:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchEmployees();
  }, [oid]);

  return (
    <CommonCard title="이상 사용자 목록">
      {loading ? (
        <Box display="flex" justifyContent="center" alignItems="center" height={150}>
          <CircularProgress />
        </Box>
      ) : (
        <Box height={300} overflow="auto">
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>사용자 ID</TableCell>
                <TableCell>이름</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {employees.map((employee) => (
                <TableRow key={employee.employee_id}>
                  <TableCell>{employee.employee_id}</TableCell>
                  <TableCell>{employee.employee_name}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Box>
      )}
    </CommonCard>
  );
};

export default AnomalyEmployeeList;