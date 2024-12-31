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
    const [teamMembers, setTeamMembers] = useState([]); // 保存已驗證的隊員

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleTeamMemberAdd = (e) => {
        e.preventDefault();
        const studentId = formData.team_info.trim();
        if (!studentId) {
            alert("請輸入隊員學號！");
            return;
        }

        axios.post("http://127.0.0.1:5000/api/accounts/check", { student_id: studentId })
            .then(response => {
                const newMember = response.data.data;
                setTeamMembers([...teamMembers, newMember]);
                alert(`隊員 ${newMember.name} 已新增！`);
                setFormData({ ...formData, team_info: "" }); // 清空輸入框
            })
            .catch(error => {
                if (error.response) {
                    alert(`錯誤：${error.response.data.message}`);
                } else {
                    console.error("Error checking team member:", error);
                    alert("檢查失敗，請稍後再試");
                }
            });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const finalFormData = { ...formData, team_members: teamMembers };

        axios.post("http://127.0.0.1:5000/api/works/Enroll", finalFormData)
            .then(response => {
                alert(response.data.message);
                setFormData({
                    competition: "2025 創意競賽",
                    name: "",
                    student_id: "",
                    department: "",
                    email: "",
                    phone: "",
                    team_info: ""
                });
                setTeamMembers([]); // 清空隊員列表
            })
            .catch(error => {
                if (error.response) {
                    alert(`提交失敗：${error.response.data.message}`);
                } else {
                    console.error("Error submitting form:", error);
                    alert("提交失敗，請稍後再試");
                }
            });
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

                <label>新增隊員 (如有)</label>
                <input
                    type="text"
                    name="team_info"
                    placeholder="輸入隊員學號"
                    value={formData.team_info}
                    onChange={handleChange}
                />
                <button onClick={handleTeamMemberAdd}>檢查並新增</button>

                <ul>
                    {teamMembers.map((member, index) => (
                        <li key={index}>{`${member.name} (${member.student_id})`}</li>
                    ))}
                </ul>

                <button type="submit">提交報名</button>
            </form>
        </div>
    );
};

export default EnrollForm;
