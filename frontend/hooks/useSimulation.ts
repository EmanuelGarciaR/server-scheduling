import { useState, useEffect, useCallback } from 'react';

export interface SimulationState {
    simulationTime: number;
    isSimulating: boolean;
    speedMultiplier: number;
}

export function useSimulation(maxTime: number) {
    const [simulationTime, setSimulationTime] = useState(0);
    const [isSimulating, setIsSimulating] = useState(false);
    const [speedMultiplier, setSpeedMultiplier] = useState(1);

    useEffect(() => {
        let interval: NodeJS.Timeout;

        if (isSimulating && simulationTime < maxTime) {
            // Base speed is 500ms per tick.
            const tickRate = 500 / speedMultiplier;
            interval = setInterval(() => {
                setSimulationTime((prev) => {
                    if (prev >= maxTime) {
                        setIsSimulating(false);
                        return maxTime;
                    }
                    return prev + 1;
                });
            }, tickRate);
        } else if (simulationTime >= maxTime) {
            setIsSimulating(false);
        }

        return () => {
            if (interval) clearInterval(interval);
        };
    }, [isSimulating, simulationTime, maxTime, speedMultiplier]);

    const play = useCallback(() => {
        if (simulationTime < maxTime) {
            setIsSimulating(true);
        }
    }, [simulationTime, maxTime]);

    const pause = useCallback(() => setIsSimulating(false), []);

    const reset = useCallback(() => {
        setIsSimulating(false);
        setSimulationTime(0);
    }, []);

    const setSpeed = useCallback((speed: number) => setSpeedMultiplier(speed), []);

    return {
        simulationTime,
        isSimulating,
        speedMultiplier,
        play,
        pause,
        reset,
        setSpeed,
        state: {
            simulationTime,
            isSimulating,
            speedMultiplier
        }
    };
}
