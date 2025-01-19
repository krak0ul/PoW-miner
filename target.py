from utils import avg_mine_time

class Target:

    def __init__(self, difficulty_period, target):
        self.difficulty_period = difficulty_period
        self.target = target
    
    def get_long_target(self):
        exponent = (self.target >> 24) & 0xFF
        significand = self.target & 0xFFFFFF
        # Calculate the long target
        long_target = significand * (2 ** (8 * (exponent - 3)))      # substract 3 to exponent because significand represents the first 3 bytes of target
        return long_target

    def get_short_target(self, long_target):
        exponent = (long_target.bit_length() + 7) // 8
        significand = long_target >> (8 * (exponent - 3))

        # Ensure the significand remains within valid bounds
        if significand > 0xFFFFFF:
            significand >>= 1
            exponent += 1
        elif significand == 0:
            significand = 1

        self.target = (exponent << 24) | significand
        return self.target


    def compute_difficulty(self, average_time, block_time_target):
        """computes new difficulty for the mining algo"""

        ratio = average_time / block_time_target

        # Restrict the adjustment ratio to avoid drastic changes - like Bitcoin
        # ratio = min(max(ratio, 0.25), 4)
        print(f"ratio: {ratio}")
        
        new_long_target = int(self.get_long_target() * ratio)
        self.target = self.get_short_target(new_long_target)

        return self.target
    
    def difficulty(self, block_chain, block_time_target):
        if len(block_chain) % self.difficulty_period == 0:
            average_time = avg_mine_time(block_chain, self.difficulty_period)
            print("------------------------------------------------------")
            print("Computing new target")
            print(f"Average block time: {average_time}")
            print(f"old target: {hex(self.get_long_target())}")
            self.compute_difficulty(average_time, block_time_target)
            print(f"new target: {hex(self.get_long_target())}")
            print("------------------------------------------------------")
        return