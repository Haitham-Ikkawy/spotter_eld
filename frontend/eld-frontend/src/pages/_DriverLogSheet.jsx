import React, {useEffect, useState} from "react";
import {Card, CardContent, Container} from "@mui/material";
import {format} from "date-fns";
import {Timeline, TimelineConnector, TimelineContent, TimelineDot, TimelineItem, TimelineSeparator} from "@mui/lab";
import {GetDriverLogSheet} from "../services/Api.js";
import {toast} from "react-toastify";
import PageTitle from "../components/shared/PageTitle.jsx";


const DriverLogSheet = ({driverId, date}) => {
    const [logData, setLogData] = useState(null);
    const [loading, setLoading] = useState(true);

    // useEffect(() => {
    //     if (!driverId || !date) return;
    //
    //     setLoading(true);
    //     axios.get(`${API_URL}?driver_id=${driverId}&date=${date}`)
    //         .then(response => {
    //             setLogData(response.data);
    //         })
    //         .catch(error => {
    //             console.error("Error fetching log data:", error);
    //         })
    //         .finally(() => {
    //             setLoading(false);
    //         });
    // }, [driverId, date]);

    useEffect(() => {
        GetDriverLogSheet({})
            .then((response) => {
                setLogData(response.data);
                console.log("response.data", response.data)
            })
            .catch((error) => {
                toast.error(error.response);
            });
    }, [driverId, date]);

    // if (loading) {
    //     return <div className="flex justify-center items-center h-64"><Loader className="animate-spin" size={32}/></div>;
    // }
    //
    // if (!logData || logData.actions.length === 0) {
    //     return <div className="text-center text-gray-500 mt-10">No log data available for this date.</div>;
    // }

    return (


        <Container>
            {logData &&
                <>

                    <PageTitle title={`Log Sheet for ${logData.driver.name} (${format(new Date(logData.date), "PPP")}`}/>
                    <Card className="p-4">

                        <Timeline position="alternate">
                            {logData.actions.map((action, index) => (
                                <TimelineItem key={index}>
                                    <TimelineSeparator>
                                        <TimelineDot color={action.status === "Off Duty" ? "grey" : "primary"}/>
                                        {index !== logData.actions.length - 1 && <TimelineConnector/>}
                                    </TimelineSeparator>
                                    <TimelineContent>
                                        <CardContent className="bg-gray-100 rounded-lg p-3 shadow-sm">
                                            <h3 className="text-lg font-semibold">{action.type}</h3>
                                            <p className="text-gray-600 text-sm">{format(new Date(action._dt), "hh:mm a")}</p>
                                            {action.location && (
                                                <p className="text-gray-500 text-sm">{action.location.name}</p>
                                            )}
                                            {action.duration && (
                                                <p className="text-gray-500 text-sm">Duration: {action.duration} mins</p>
                                            )}
                                            <p className={`text-sm font-medium ${action.status === "Off Duty" ? "text-red-500" : "text-green-600"}`}>
                                                Status: {action.status}
                                            </p>
                                            <p className="text-gray-500 text-sm">Odometer: {action.odometer} miles</p>
                                        </CardContent>
                                    </TimelineContent>
                                </TimelineItem>
                            ))}
                        </Timeline>
                    </Card>
                </>
            }
        </Container>
    )
};

export default DriverLogSheet;
