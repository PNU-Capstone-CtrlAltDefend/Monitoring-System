const API_URL = process.env.REACT_APP_API_URL;

/**
 * 기간을 받아 이상 사용자 탐지 결과를 조회합니다.
 */
export async function fetchAnomalyDetection({ organizationId, startDate, endDate }) {
  const token = localStorage.getItem('access_token');
  const url = `${API_URL}/anomalydetect/${organizationId}/?start_dt=${startDate}T00:00:00&end_dt=${endDate}T00:00:00`;
  const response = await fetch(url, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!response.ok) throw new Error('이상 탐지 데이터를 가져오는 데 실패했습니다.');
  return await response.json();
}