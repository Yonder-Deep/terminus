import time


class AUVPID:
    """PID Controller"""

    def __init__(self, target, p=0.2, i=0.0, d=0.0, i_windup=20.0):
        # Initialize parameters
        self.set_point = target
        self.p = p
        self.i = i
        self.d = d
        self.windup = i_windup

        self.last_error = 0.0
        self.sum_error = 0.0
        self.last_time = time.time()

    def pid(self, current_value):
        """PID Calculation"""
        # Calculate error
        error = self.set_point - current_value
        dt = time.time() - self.last_time

        # Calculate P term
        p_term = self.p * error
        # Calculate I term
        self.sum_error += error * (time.time() - self.last_time)
        i_change = self.sum_error if abs(self.sum_error) < self.windup else (
            self.windup if self.sum_error >= 0 else -self.windup)
        i_change *= dt
        i_term = self.i * i_change
        # Calculate D term
        d_term = self.d * (error - self.last_error)
        d_term /= dt

        # Update values for next iteration
        self.last_time = time.time()
        self.last_error = error

        return p_term + i_term + d_term  # pid

    def set_p(self, p):
        self.p = p

    def set_i(self, i):
        self.i = i

    def set_d(self, d):
        self.d = d

    def set_windup(self, windup):
        """Integral windup, also known as integrator windup or reset windup,
        refers to the situation in a PID feedback controller where
        a large change in setpoint occurs (say a positive change)
        and the integral terms accumulates a significant error
        during the rise (windup), thus overshooting and continuing
        to increase as this accumulated error is unwound
        (offset by errors in the other direction).
        The specific problem is the excess overshooting.
        """
        self.windup = windup

    def update_target(self, target):
        self.set_point = target
