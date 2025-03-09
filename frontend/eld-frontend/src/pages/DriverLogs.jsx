import React from 'react';
import DownloadLogSheet from '../components/LogSheet.jsx';

function DriverLogs() {
  const driver = {
    name: 'John Doe',
    licenseNumber: 'D1234567',
    currentCycleUsed: 10,
  };

  const trip = {
    id: 1,
    startLocation: 'New York',
    endLocation: 'Los Angeles',
    startTime: '2023-10-01T08:00:00Z',
    endTime: '2023-10-02T08:00:00Z',
    distance: 2800,
    remarks: 'No issues during the trip.',
  };

  const logs = [
    { date: '2023-10-01', totalDrivingHours: 8, totalOnDutyHours: 10 },
    { date: '2023-10-02', totalDrivingHours: 7, totalOnDutyHours: 9 },
  ];

  return (
    <div>
      <h1>Driver Logs</h1>
      <DownloadLogSheet driver={driver} trip={trip} logs={logs} />
    </div>
  );
}

export default DriverLogs;