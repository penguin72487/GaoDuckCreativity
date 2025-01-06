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
        team_member1: "",
        team_member2: "",
        team_member3: "",
        team_member4: "",
        team_member5: ""
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        const teacherId = formData.teacher_id.trim();
        if (!teacherId) {
            alert("請輸入指導教授帳號！");
            return;
        }

        const teamMemberIds = [
            formData.team_member1 || null, 
            formData.team_member2 || null, 
            formData.team_member3 || null,
            formData.team_member4 || null,
            formData.team_member5 || null
        ];

        const validTeamMemberIds = teamMemberIds.filter(Boolean);

        if (validTeamMemberIds.length === 0) {
            alert("請至少新增一名隊員！");
            return;
        }

        if (validTeamMemberIds.length > 5) {
            alert("最多只能新增5名隊員！");
            return;
        }

        // 檢查指導教授帳號
        axios.post("http://127.0.0.1:5000/api/accounts/check", { u_id: teacherId })
            .then(response => {
                const teacher = response.data.data;
                if (teacher.role !== 2 && teacher.role !== 3) { // 將 role 與整數進行比較
                    alert("該使用者不是教授，請輸入有效教授帳號！");
                    return;
                }

                // 檢查隊員帳號
                console.log("Valid team member IDs:", validTeamMemberIds);
                const checkTeamMembers = validTeamMemberIds.map(id => 
                    axios.post("http://127.0.0.1:5000/api/accounts/check", { u_id: id })
                        .then(response => response.data.data)
                        .catch(error => {
                            if (error.response) {
                                alert(`錯誤：${error.response.data.message || "未知錯誤"}`);
                            } else {
                                console.error("Error checking team member:", error);
                                alert("檢查失敗，請稍後再試");
                            }
                            throw error;
                        })
                );

                Promise.all(checkTeamMembers)
                    .then(members => {
                        const finalFormData = { 
                            ...formData, 
                            teacher, 
                            team_members: members 
                        };

                        axios.post("http://127.0.0.1:5000/api/submit_project", finalFormData) // 更新 API 路由
                            .then(response => {
                                console.log("Submission response:", response.data);
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
                                    team_member1: "",
                                    team_member2: "",
                                    team_member3: "",
                                    team_member4: "",
                                    team_member5: ""
                                });
                            })
                            .catch(error => {
                                if (error.response) {
                                    alert(`提交失敗：${error.response.data.message || "未知錯誤"}`);
                                } else {
                                    console.error("Error submitting form:", error);
                                    alert("提交失敗，請稍後再試");
                                }
                            });
                    })
                    .catch(() => {
                        // 已在個別檢查中處理錯誤
                    });
            })
            .catch(error => {
                if (error.response) {
                    alert(`錯誤：${error.response.data.message || "未知錯誤"}`);
                } else {
                    console.error("Error checking teacher:", error);
                    alert("檢查失敗，請稍後再試");
                }
            });
    };

    return (
        <div className="page">
            <h1>報名表單</h1>
            <form onSubmit={handleSubmit}>
                <label>競賽名稱</label>
                <select name="competition" value={formData.competition} onChange={handleChange}>
                    <option>2025 創意競賽</option>
                </select>

                <label>隊伍名稱</label>
                <input type="text" name="name" placeholder="輸入隊伍名稱" value={formData.name} onChange={handleChange} />

                <label>隊長帳號</label>
                <input type="text" name="student_id" placeholder="輸入隊長帳號" value={formData.student_id} onChange={handleChange} />
                <label>競賽組別</label>
                <select name="competition_group" value={formData.competition_group} onChange={handleChange}>
                    <option>創意發想組</option>
                    <option>創業實作組</option>
                </select>

                <label>作品說明書</label>
                <input type="file" name="description" onChange={handleChange} />

                <label>作品海報</label>
                <input type="file" name="poster" onChange={handleChange} />
                    
                <label>作品Demo影片(Youtube連結)</label>
                <input type="text" name="video" placeholder="輸入Youtube連結" value={formData.video} onChange={handleChange} />

                <label>程式碼(Github連結)</label>
                <input type="text" name="code" placeholder="輸入Github連結" value={formData.code} onChange={handleChange} />

                <label>指導教授帳號</label>
                <input
                    type="text"
                    name="teacher_id"
                    placeholder="輸入指導教授帳號"
                    value={formData.teacher_id}
                    onChange={handleChange}
                />
                {formData.teacher && (
                    <p>已確認指導教授：{formData.teacher.name} ({formData.teacher.u_id})</p>
                )}

                <label>隊員1帳號</label>
                <input
                    type="text"
                    name="team_member1"
                    placeholder="輸入隊員1帳號"
                    value={formData.team_member1}
                    onChange={handleChange}
                />

                <label>隊員2帳號</label>
                <input
                    type="text"
                    name="team_member2"
                    placeholder="輸入隊員2帳號"
                    value={formData.team_member2}
                    onChange={handleChange}
                />

                <label>隊員3帳號</label>
                <input
                    type="text"
                    name="team_member3"
                    placeholder="輸入隊員3帳號"
                    value={formData.team_member3}
                    onChange={handleChange}
                />

                <label>隊員4帳號</label>
                <input
                    type="text"
                    name="team_member4"
                    placeholder="輸入隊員4帳號"
                    value={formData.team_member4}
                    onChange={handleChange}
                />

                <label>隊員5帳號</label>
                <input
                    type="text"
                    name="team_member5"
                    placeholder="輸入隊員5帳號"
                    value={formData.team_member5}
                    onChange={handleChange}
                />

                <button type="submit">提交報名</button>
            </form>
        </div>
    );
};

export default EnrollForm;