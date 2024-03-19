from simulation_manager import SimulationManager

def main():
    simulation_manager = SimulationManager()
    cell_size = 10
    total_movement_unit = 1000
    simulation_manager.run(cell_size, total_movement_unit)

if __name__ == "__main__":
    main()
