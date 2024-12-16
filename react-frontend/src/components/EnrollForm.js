import React, { useState } from "react";
import axios from "axios";

const EnrollForm = () => {
    const [formData, setFormData] = useState({
        competition: "2025 創意競賽",
        name: "",
        student_id: "",
        department: "",
        email: "",
        phone: "",
        team_info: ""
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post("http://127.0.0.1:5000/api/enroll", formData)
            .then(response => alert(response.data.message))
            .catch(error => console.error("Error submitting form:", error));
    };

    return (
        <div className="page">
            <h1>報名表單</h1>
            <form onSubmit={handleSubmit}>
                <label>競賽名稱</label>
                <select name="competition" onChange={handleChange}>
                    <option>2025 創意競賽</option>
                </select>

                <label>姓名</label>
                <input type="text" name="name" onChange={handleChange} />

                <label>學號</label>
                <input type="text" name="student_id" onChange={handleChange} />

                <label>系所</label>
                <input type="text" name="department" onChange={handleChange} />

                <label>Email</label>
                <input type="email" name="email" onChange={handleChange} />

                <label>聯絡電話</label>
                <input type="text" name="phone" onChange={handleChange} />

                <label>隊員資訊 (如有)</label>
                <textarea name="team_info" onChange={handleChange}></textarea>

                <button type="submit">提交報名</button>
            </form>
        </div>
    );
};

export default EnrollForm;
