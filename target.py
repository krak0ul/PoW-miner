class Target:

    def __init__(self, target):
        self.target = target
        

    
    def get_long_target(self):
        exponent = (self.target >> 24) & 0xFF
        significand = self.target & 0xFFFFFF

        # Calculate the long target
        long_target = significand * (2 ** (8 * (exponent - 3)))      # substract 3 to exponent because significand represents the first 3 bytes of target
        return str(long_target)

    def get_short_target(self, long_target):
        exponent = (long_target.bit_length() + 7) // 8
        mantissa = long_target >> (8 * (exponent - 3))
        self.target = (exponent << 24) | mantissa
        return self.target


    def compute_difficulty(self, average_time, block_time_target):
        """Simplifies the difficulty adjustment logic."""

        ratio = block_time_target / average_time

        # Clamp the adjustment ratio to avoid drastic changes
        # ratio = min(max(ratio, 0.25), 4)
        print(ratio)
        
        # Adjust the significand directly
        significand = self.target & 0xFFFFFF         # lower 24 bits - precise value of target
        exponent = (self.target >> 24) & 0xFF        # select most significant byte only

        # Scale the significand based on the adjustment ratio
        new_significand = int(significand / ratio)

        # Ensure the significand remains within valid bounds
        if new_significand > 0xFFFFFF:
            new_significand >>= 1
            exponent += 1
        elif new_significand == 0:
            new_significand = 1

        # Reconstruct the new target value
        self.target = (exponent << 24) | (new_significand & 0xFFFFFF)
        return self.target