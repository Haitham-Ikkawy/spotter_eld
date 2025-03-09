import React from 'react';
import { PDFDownloadLink, Document, Page, Text, View, StyleSheet } from '@react-pdf/renderer';

// Define styles for the PDF
const styles = StyleSheet.create({
  page: {
    padding: 20,
    fontFamily: 'Helvetica',
  },
  header: {
    fontSize: 18,
    marginBottom: 10,
    textAlign: 'center',
    fontWeight: 'bold',
  },
  section: {
    marginBottom: 10,
  },
  table: {
    display: 'flex',
    flexDirection: 'row',
    borderBottomWidth: 1,
    borderBottomColor: '#000',
    borderBottomStyle: 'solid',
    marginBottom: 10,
  },
  tableHeader: {
    fontWeight: 'bold',
    backgroundColor: '#f0f0f0',
    padding: 5,
  },
  tableCell: {
    padding: 5,
    flex: 1,
    borderRightWidth: 1,
    borderRightColor: '#000',
    borderRightStyle: 'solid',
  },
  remarks: {
    marginTop: 10,
    fontStyle: 'italic',
  },
});

// LogSheet Component
const LogSheet = ({ driver, trip, logs }) => (
  <Document>
    <Page size="A4" style={styles.page}>
      {/* Header */}
      <Text style={styles.header}>Driver's Daily Log</Text>

      {/* Driver Information */}
      <View style={styles.section}>
        <Text>Driver: {driver.name}</Text>
        <Text>License Number: {driver.licenseNumber}</Text>
        <Text>Current Cycle Used: {driver.currentCycleUsed} hours</Text>
      </View>

      {/* Trip Information */}
      <View style={styles.section}>
        <Text>Trip ID: {trip.id}</Text>
        <Text>Start Location: {trip.startLocation}</Text>
        <Text>End Location: {trip.endLocation}</Text>
        <Text>Start Time: {trip.startTime}</Text>
        <Text>End Time: {trip.endTime}</Text>
        <Text>Distance: {trip.distance} miles</Text>
      </View>

      {/* Log Table */}
      <View style={styles.section}>
        <Text style={styles.tableHeader}>Driving Logs</Text>
        <View style={styles.table}>
          <Text style={styles.tableCell}>Date</Text>
          <Text style={styles.tableCell}>Total Driving Hours</Text>
          <Text style={styles.tableCell}>Total On-Duty Hours</Text>
        </View>
        {logs.map((log, index) => (
          <View key={index} style={styles.table}>
            <Text style={styles.tableCell}>{log.date}</Text>
            <Text style={styles.tableCell}>{log.totalDrivingHours}</Text>
            <Text style={styles.tableCell}>{log.totalOnDutyHours}</Text>
          </View>
        ))}
      </View>

      {/* Remarks */}
      <View style={styles.section}>
        <Text style={styles.remarks}>Remarks: {trip.remarks}</Text>
      </View>
    </Page>
  </Document>
);

// Download Link Component
const DownloadLogSheet = ({ driver, trip, logs }) => (
  <PDFDownloadLink document={<LogSheet driver={driver} trip={trip} logs={logs} />} fileName="driver_log.pdf">
    {({ loading }) => (loading ? 'Loading document...' : 'Download Log Sheet')}
  </PDFDownloadLink>
);

export default DownloadLogSheet;