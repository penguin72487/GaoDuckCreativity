import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
    const [data, setData] = useState(null);

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/api/data') // Flask API 路徑
            .then(response => {
                setData(response.data.message);
            })
            .catch(error => {
                console.error("Error fetching data: ", error);
            });
    }, []);

    return (
        <div className="App">
            <h1>React + Flask</h1>
            <p>{data ? data : "Loading..."}</p>
        </div>
    );
}

export default App;
