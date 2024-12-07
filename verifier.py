import json

def verify_node_assignment(solution_json):
    """
    Verifies that every node is assigned to exactly one vehicle.

    Parameters:
        solution_json (dict): The JSON solution containing assignment data.

    Returns:
        dict: Summary of the verification.
    """
    # Parse the 'z' dictionary from the solution
    z = solution_json.get("z", {})
    
    # Dictionary to track assignments per node
    node_assignments = {}
    
    for key, value in z.items():
        # Parse the node and vehicle from the key
        node, vehicle = eval(key)
        
        # Initialize the node in the assignments dictionary if not present
        if node not in node_assignments:
            node_assignments[node] = 0
        
        # Increment assignment count if this pair is assigned (value == 1)
        if value == 1:
            node_assignments[node] += 1
    
    # Analyze results
    unassigned_nodes = [node for node, count in node_assignments.items() if count == 0]
    overassigned_nodes = [node for node, count in node_assignments.items() if count > 1]
    assigned_nodes = [node for node, count in node_assignments.items() if count == 1]

    # Output the verification result
    result = {
        "TotalNodes": len(node_assignments),
        "AssignedNodes": len(assigned_nodes),
        "UnassignedNodes": unassigned_nodes,
        "OverassignedNodes": overassigned_nodes,
    }
    return result

# Example usage
if __name__ == "__main__":
    # Load the solution JSON (replace 'output.json' with your file)
    with open("C:\\Users\\cdcp2\\Desktop\\MOS\\proyecto_e2\\output2.json", "r", encoding='utf-8') as f:
        solution_data = json.load(f)

    
    # Verify assignments
    verification_result = verify_node_assignment(solution_data)
    
    # Display the results
    print("Verification Result:")
    print(json.dumps(verification_result, indent=4))
