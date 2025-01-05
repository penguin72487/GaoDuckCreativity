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
        teacher_id: "",
        teacher: null,
        team_members: [],
    });
    const [teamMembers, setTeamMembers] = useState([]);

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
                setFormData({ ...formData, team_info: "" });
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

    const handleTeacherCheck = (e) => {
        e.preventDefault();
        const teacherId = formData.teacher_id.trim();
        if (!teacherId) {
            alert("請輸入指導教授學號！");
            return;
        }

        axios.post("http://127.0.0.1:5000/api/accounts/check", { student_id: teacherId })
            .then(response => {
                const teacher = response.data.data;
                if (teacher.role !== 99 && teacher.role !== 3) {
                    alert("該使用者不是教授，請輸入有效教授學號！");
                    return;
                }
                setFormData({ ...formData, teacher });
                alert(`指導教授 ${teacher.name} 已確認！`);
            })
            .catch(error => {
                if (error.response) {
                    alert(`錯誤：${error.response.data.message}`);
                } else {
                    console.error("Error checking teacher:", error);
                    alert("檢查失敗，請稍後再試");
                }
            });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!formData.teacher) {
            alert("請先確認指導教授！");
            return;
        }
        const finalFormData = { 
            ...formData, 
            teacher: formData.teacher, 
            team_members: teamMembers 
        };

        axios.post("http://127.0.0.1:5000/api/projects/Enroll", finalFormData)
            .then(response => {
                alert(response.data.message);
                setFormData({
                    competition: "2025 創意競賽",
                    name: "",
                    student_id: "",
                    department: "",
                    email: "",
                    phone: "",
                    teacher_id: "",
                    teacher: null,
                    team_members: [],
                });
                setTeamMembers([]);
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

                <label>隊伍名稱</label>
                <input type="text" name="name" placeholder="輸入隊伍名稱" value={formData.name} onChange={handleChange} />

                <label>隊長學號</label>
                <input type="text" name="student_id" placeholder="輸入隊長學號" value={formData.student_id} onChange={handleChange} />
                <label>競賽組別</label>
                <select name="competition_group" onChange={handleChange}>
                    <option>創意發想組</option>
                    <option>創業實作組</option>
                </select>

                <label>作品說明書</label>
                <input type="file" name="description" onChange={handleChange} />

                <label>作品海報</label>
                <input type="file" name="poster" onChange={handleChange} />
                    
                <label>作品Demo影片(Youtube連結)選填</label>
                <input type="text" name="video" placeholder="輸入Youtube連結" value={formData.video} onChange={handleChange} />

                <label> 程式碼(Github連結)選填</label>
                <input type="text" name="code" placeholder="輸入Github連結" value={formData.code} onChange={handleChange} />


                <label>指導教授學號</label>
                <input
                    type="text"
                    name="teacher_id"
                    placeholder="輸入指導教授學號"
                    value={formData.teacher_id}
                    onChange={handleChange}
                />
                <button onClick={handleTeacherCheck}> 新增指導教授</button>
                {formData.teacher && (
                    <p>已確認指導教授：{formData.teacher.name} ({formData.teacher.student_id})</p>
                )}

                <label>新增隊員 (如有)</label>
                <input
                    type="text"
                    name="team_info"
                    placeholder="輸入隊員學號"
                    value={formData.team_info}
                    onChange={handleChange}
                />
                <button onClick={handleTeamMemberAdd}>新增隊員</button>

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
