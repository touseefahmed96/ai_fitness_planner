import React, { useEffect, useState } from "react";

function Workout() {
    const [userId, setUserId] = useState<number | null>(null);
    const [fitnessLevel, setFitnessLevel] = useState<string>("beginner");
    const [goal, setGoal] = useState<string | null>(null);
    const [workoutPlan, setWorkoutPlan] = useState<any | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const token = localStorage.getItem("token");

        if (!token) {
            window.location.href = "/login";  // Redirect to login if no token
        } else {
            fetch("http://localhost:8000/api/v1/user/me", {
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    setUserId(data.id);
                    setGoal(data.goal);
                    setLoading(false);
                })
                .catch(() => {
                    setError("Failed to fetch user data");
                    setLoading(false);
                });
        }
    }, []);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (userId && fitnessLevel && goal) {
            setLoading(true);
            setError(null);

            fetch("http://localhost:8000/api/v1/workout/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`,
                },
                body: JSON.stringify({
                    user_id: userId,
                    fitness_level: fitnessLevel,
                    goal: goal,
                }),
            })
                .then((response) => response.json())
                .then((data) => {
                    setWorkoutPlan(data.workout_plan);
                    setLoading(false);
                })
                .catch(() => {
                    setError("Failed to load workout plan");
                    setLoading(false);
                });
        } else {
            setError("Please provide valid input.");
        }
    };

    if (loading) {
        return <div>Loading your workout plan...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div className="form-container">
            <h2>Your Personalized Workout Plan</h2>

            {workoutPlan ? (
                <div className="workout-plan">
                    <div className="section">
                        <h3>Warm-up</h3>
                        <ul>
                            <li>Light cardio: 5-10 minutes on the treadmill, stationary bike, or elliptical machine</li>
                            <li>Dynamic stretching: Focus on major muscle groups (legs, hips, back, chest, shoulders, arms)</li>
                        </ul>
                    </div>

                    <div className="section">
                        <h3>Monday (Chest and Triceps)</h3>
                        <ul>
                            <li>Barbell Bench Press: 3 sets of 8-12 reps</li>
                            <li>Incline Dumbbell Press: 3 sets of 10-15 reps</li>
                            <li>Cable Fly: 3 sets of 12-15 reps</li>
                            <li>Tricep Pushdown: 3 sets of 10-12 reps</li>
                            <li>Overhead Dumbbell Extension: 3 sets of 12-15 reps</li>
                            <li>Close-Grip Bench Press: 3 sets of 8-10 reps</li>
                        </ul>
                    </div>

                    <div className="section">
                        <h3>Tuesday (Back and Biceps)</h3>
                        <ul>
                            <li>Pull-ups: 3 sets of 8-12 reps</li>
                            <li>Barbell Rows: 3 sets of 8-12 reps</li>
                            <li>Lat Pulldowns: 3 sets of 10-12 reps</li>
                            <li>Dumbbell Bicep Curls: 3 sets of 10-12 reps</li>
                            <li>Hammer Curls: 3 sets of 10-12 reps</li>
                            <li>Preacher Curls: 3 sets of 10-12 reps</li>
                        </ul>
                    </div>

                    <div className="section">
                        <h3>Wednesday (Rest Day)</h3>
                        <p>Rest and recovery</p>
                    </div>

                    <div className="section">
                        <h3>Thursday (Legs)</h3>
                        <ul>
                            <li>Squats: 3 sets of 8-12 reps</li>
                            <li>Leg Press: 3 sets of 10-12 reps</li>
                            <li>Lunges: 3 sets of 10-12 reps</li>
                            <li>Leg Extensions: 3 sets of 12-15 reps</li>
                            <li>Leg Curls: 3 sets of 10-12 reps</li>
                            <li>Calf Raises: 3 sets of 12-15 reps</li>
                        </ul>
                    </div>

                    <div className="section">
                        <h3>Friday (Shoulders and Abs)</h3>
                        <ul>
                            <li>Standing Military Press: 3 sets of 8-12 reps</li>
                            <li>Seated Dumbbell Shoulder Press: 3 sets of 10-12 reps</li>
                            <li>Lateral Raises: 3 sets of 10-12 reps</li>
                            <li>Rear Delt Fly: 3 sets of 12-15 reps</li>
                            <li>Planks: 3 sets of 30-60 seconds</li>
                            <li>Russian Twists: 3 sets of 10-12 reps</li>
                        </ul>
                    </div>

                    <div className="section">
                        <h3>Saturday and Sunday (Rest Days)</h3>
                        <p>Rest and recovery</p>
                    </div>

                    <div className="section">
                        <h3>Progressive Overload</h3>
                        <p>Increase the weight you lift by 2.5-5lbs every two weeks to help build strength and muscle mass.</p>
                    </div>

                    <div className="section">
                        <h3>Nutrition</h3>
                        <ul>
                            <li>Protein: 1.2-1.6 grams per kilogram of body weight</li>
                            <li>Carbohydrates: 2-3 grams per kilogram of body weight</li>
                            <li>Healthy Fats: 0.5-1 gram per kilogram of body weight</li>
                            <li>Eat 5-6 meals per day, spaced out every 2-3 hours</li>
                        </ul>
                    </div>

                    <div className="section">
                        <h3>Supplements</h3>
                        <ul>
                            <li>Protein Powder: To support muscle growth and recovery</li>
                            <li>Mass Gainer: To increase calorie intake and support muscle growth</li>
                            <li>Creatine: To increase strength and endurance</li>
                        </ul>
                    </div>

                    <div className="section">
                        <h3>Tips and Reminders</h3>
                        <ul>
                            <li>Warm up properly before each workout</li>
                            <li>Focus on proper form and technique</li>
                            <li>Increase weight and reps as you get stronger</li>
                            <li>Rest and recover adequately between workouts</li>
                            <li>Stay hydrated and fuel your body with a balanced diet</li>
                        </ul>
                    </div>
                </div>
            ) : (
                <form onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="fitnessLevel">Select Fitness Level:</label>
                        <select
                            id="fitnessLevel"
                            value={fitnessLevel}
                            onChange={(e) => setFitnessLevel(e.target.value)}
                            required
                        >
                            <option value="beginner">Beginner</option>
                            <option value="intermediate">Intermediate</option>
                            <option value="advanced">Advanced</option>
                        </select>
                    </div>

                    <button type="submit">Generate Workout Plan</button>
                </form>
            )}
        </div>
    );
}

export default Workout;
