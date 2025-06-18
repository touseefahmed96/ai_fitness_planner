import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Signup() {
    const navigate = useNavigate();
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [goal, setGoal] = useState("");
    const [weight, setWeight] = useState("");
    const [height, setHeight] = useState("");
    const [error, setError] = useState("");

    const handleSignup = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        try {
            const response = await fetch("http://localhost:8000/api/v1/user/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ name, email, password, goal, weight, height }),
            });

            if (!response.ok) {
                throw new Error("Registration failed");
            }

            navigate("/login");
        } catch (err: any) {
            setError(err.message || "Signup failed");
        }
    };

    return (
        <div className="form-container">
            <h2>Sign Up</h2>
            <form onSubmit={handleSignup}>
                <input
                    type="text"
                    placeholder="Full Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <input
                    type="text"
                    placeholder="Fitness Goal"
                    value={goal}
                    onChange={(e) => setGoal(e.target.value)}
                    required
                />
                <input
                    type="number"
                    placeholder="Weight (kg)"
                    value={weight}
                    onChange={(e) => setWeight(e.target.value)}
                    required
                />
                <input
                    type="number"
                    placeholder="Height (cm)"
                    value={height}
                    onChange={(e) => setHeight(e.target.value)}
                    required
                />
                <button type="submit">Sign Up</button>
                {error && <p className="error-message">{error}</p>}
            </form>
            <div className="link">
                <p>Already have an account? <a href="/login">Login</a></p>
            </div>
        </div>
    );
}

export default Signup;
