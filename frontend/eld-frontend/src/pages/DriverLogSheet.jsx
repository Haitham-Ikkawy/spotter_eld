import React, {useEffect, useRef, useState} from "react";
import {Box, Container, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Typography} from "@mui/material";
import PageTitle from "../components/shared/PageTitle.jsx";
import {GetDriverLogSheet} from "../services/Api.js";
import {toast} from "react-toastify";

const STATUS_COLORS = {
    "Off Duty": "#ADD8E6", // Light Blue
    "Sleeper Berth": "#4682B4", // Darker Blue
    "Driving": "#FFFF99", // Light Yellow
    "On Duty": "#FFD700" // Lighter Yellow
};


const ROW_POSITIONS = {"Off Duty": 0, "Sleeper Berth": 1, "Driving": 2, "On Duty": 3};

const DriverLogSheet = () => {


    const [logData, setLoggData] = useState(null);
    const [queryParams, setQueryParams] = useState({date:new Date().toISOString().split("T")[0] });


    useEffect(() => {

        if (queryParams.date) {
            GetDriverLogSheet(queryParams)
                .then((response) => {
                    setLoggData(response.data);
                    console.log("response.data", response.data)
                })
                .catch((error) => {
                    toast.error(error.response);
                });
        }

    }, [queryParams]);

    // const logData = {
    //     driver: {name: "John Doe", license: "ABC123456"},
    //     date: "2025-03-22",
    //     logs: [
    //         {startHour: 0, endHour: 3.25, status: "Off Duty"},
    //         {startHour: 3.25, endHour: 7, status: "Sleeper Berth"},
    //         {startHour: 7, endHour: 9, status: "On Duty"},
    //         {startHour: 9, endHour: 12, status: "Driving"},
    //         {startHour: 12, endHour: 13, status: "On Duty"},
    //         {startHour: 13, endHour: 18, status: "Driving"},
    //         {startHour: 18, endHour: 21, status: "Sleeper Berth"},
    //         {startHour: 21, endHour: 24, status: "Off Duty"}
    //     ],
    //     trip_events: [
    //         {type: "Fuel Stop", timestamp: "2025-03-22T10:30:00Z", location: "Chicago, IL", odometer: 1200},
    //         {type: "Rest Break", timestamp: "2025-03-22T15:00:00Z", location: "Indianapolis, IN", odometer: 1500},
    //         {type: "End of Day", timestamp: "2025-03-22T23:30:00Z", location: "Columbus, OH", odometer: 1800}
    //     ],
    //     daily_recap: {
    //         total_driving_hours: "10 hrs",
    //         total_on_duty_hours: "12 hrs",
    //         hours_available_tomorrow: "14 hrs",
    //         miles_driven: "600 miles"
    //     }
    // };

    const canvasRef = useRef(null);

    // Define hourWidth outside of useEffect so it can be used in JSX
    const hourWidth = 800 / 24; // Width of each hour column (canvas width is 800)

    useEffect(() => {

        if (logData) {
            const canvas = canvasRef.current;
            const ctx = canvas.getContext("2d");
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const width = canvas.width;
            const height = canvas.height;
            const rowHeight = height / 4; // Height of each row (activity type)

            // Draw background color sections
            Object.entries(ROW_POSITIONS).forEach(([status, row]) => {
                ctx.fillStyle = STATUS_COLORS[status];
                ctx.fillRect(0, row * rowHeight, width, rowHeight); // Fill the entire row with the status color
            });

            // Draw black lines to separate colored sections
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 2;
            for (let i = 1; i < 4; i++) {
                const y = i * rowHeight;
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(width, y);
                ctx.stroke();
            }

            // Draw vertical hour lines and quarter-hour lines
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 0.5;
            for (let i = 0; i <= 24; i++) {
                const x = i * hourWidth;

                // Draw hour lines (bold)
                ctx.lineWidth = 2; // Make hour lines bold
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, height);
                ctx.stroke();

                // Draw quarter-hour lines (lighter)
                ctx.lineWidth = 0.5; // Make quarter-hour lines lighter
                for (let j = 1; j < 4; j++) {
                    const quarterX = x + (j * hourWidth / 4);
                    ctx.beginPath();
                    ctx.moveTo(quarterX, 0);
                    ctx.lineTo(quarterX, height);
                    ctx.stroke();
                }
            }

            // Draw status lines
            ctx.lineWidth = 3;
            logData.logs.forEach((log, index) => {
                const startX = log.startHour * hourWidth;
                const endX = log.endHour * hourWidth;
                const y = rowHeight * ROW_POSITIONS[log.status] + rowHeight / 2;

                ctx.strokeStyle = "red";
                ctx.beginPath();
                ctx.moveTo(startX, y);
                ctx.lineTo(endX, y);
                ctx.stroke();

                // Connect to next status
                if (index < logData.logs.length - 1) {
                    const nextLog = logData.logs[index + 1];
                    const nextY = rowHeight * ROW_POSITIONS[nextLog.status] + rowHeight / 2;
                    ctx.lineTo(endX, nextY);
                    ctx.stroke();
                }
            });
        }

    }, [logData]);
    const handleInputChange = (e) => {
        const {name, value} = e.target;
        setQueryParams({...queryParams, [name]: value});
    };
    return (
        <Container>

            <PageTitle title="Driver Log Sheet"/>
            {/* Current Cycle Used */}
            <TextField type="date"
                // inputProps={{min: 0, max: 100}} // Sets UI constraints
                       label="" placeholder={""} name="date" value={queryParams.date} onChange={handleInputChange} fullWidth margin="normal" required/>
            {logData &&
                <>
                    <Box sx={{textAlign: "center", mt: 4}}>
                        <Typography variant="h6">Driver Log Sheet for {logData.driver.name}</Typography>
                        <Typography variant="subtitle1">License: {logData.driver.license}</Typography>
                        <Typography variant="subtitle1">Date: {logData.date}</Typography>

                        {/* Hours on Top */}
                        <Box sx={{display: "flex", justifyContent: "space-between", width: "100%", mt: 2}}>
                            {Array.from({length: 24}, (_, i) => (
                                <Typography
                                    key={i}
                                    variant="body2"
                                    sx={{
                                        width: `${100 / 24}%`,
                                        textAlign: "center",
                                        marginLeft: i === 0 ? "0" : `-${hourWidth / 2}px`, // Adjust alignment for the first hour
                                    }}
                                >
                                    {`${i.toString().padStart(2, '0')}:00`}
                                </Typography>
                            ))}
                        </Box>

                        {/* Grid with Section Titles on Left */}
                        <Box sx={{display: "flex", width: "100%", mt: 1}}>
                            {/* Section Titles on Left */}
                            <Box sx={{width: "100px", display: "flex", flexDirection: "column", justifyContent: "space-between"}}>
                                {Object.keys(ROW_POSITIONS).map((status) => (
                                    <Typography key={status} variant="body2" sx={{height: `${100 / 4}%`, textAlign: "left"}}>
                                        {status}
                                    </Typography>
                                ))}
                            </Box>

                            {/* Canvas Grid */}
                            <canvas ref={canvasRef} width={800} height={200} style={{border: "1px solid #000", width: "calc(100% - 100px)"}}/>
                        </Box>

                        {/* Trip Events Table */}
                        <TableContainer component={Paper} sx={{mt: 4}}>
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Type</TableCell>
                                        <TableCell>Timestamp</TableCell>
                                        <TableCell>Location</TableCell>
                                        <TableCell>Odometer</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {logData.trip_events.map((event, index) => (
                                        <TableRow key={index}>
                                            <TableCell>{event.type}</TableCell>
                                            <TableCell>{new Date(event.timestamp).toLocaleString()}</TableCell>
                                            <TableCell>{event.location}</TableCell>
                                            <TableCell>{event.odometer} miles</TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>

                        {/* Daily Recap */}
                        <Box sx={{mt: 4, p: 2, border: "1px solid #000", borderRadius: "8px"}}>
                            <Typography variant="h6">Daily Recap</Typography>
                            <Typography>Total Driving Hours: {logData.daily_recap.total_driving_hours}</Typography>
                            <Typography>Total On Duty Hours: {logData.daily_recap.total_on_duty_hours}</Typography>
                            <Typography>Hours Available Tomorrow: {logData.daily_recap.hours_available_tomorrow}</Typography>
                            <Typography>Miles Driven: {logData.daily_recap.miles_driven}</Typography>
                        </Box>

                        {/* Remarks Section */}
                        <Box sx={{mt: 4, p: 2, border: "1px solid #000", borderRadius: "8px"}}>
                            <Typography variant="h6">Remarks</Typography>
                            <Typography>1. Fuel Stop at Chicago, IL</Typography>
                            <Typography>2. Rest Break at Indianapolis, IN</Typography>
                            <Typography>3. End of Day at Columbus, OH</Typography>
                        </Box>
                    </Box>
                </>
            }

        </Container>
    );
};

export default DriverLogSheet;