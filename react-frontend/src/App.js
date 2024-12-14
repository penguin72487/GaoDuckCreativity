import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
    const [data, setData] = useState(null);
    const [input, setInput] = useState('');

    // 從後端取得資料（GET 請求）
    useEffect(() => {
        axios.get('http://127.0.0.1:5000/api/data')
            .then(response => {
                setData(response.data.message);
            })
            .catch(error => {
                console.error("Error fetching data: ", error);
            });
    }, []);

    // 發送新增資料請求（POST 請求至 /api/test）
    const handlePostData = () => {
        axios.post('http://127.0.0.1:5000/api/test', { message: input }) //範例button
            .then(response => {
                console.log('Response from backend:', response.data);
                setData(response.data.message); // 更新前端顯示
            })
            .catch(error => {
                console.error("Error posting data: ", error);
            });
    };

    return (
        <div className="App">
            <h1>React + Flask</h1>
            <div>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Enter a message"
                />
                <button onClick={handlePostData}>Send Message</button>
            </div>
            <p>{data ? data : "Loading..."}</p>
        </div>
    );
}

export default App;
