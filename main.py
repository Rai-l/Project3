
import sys
from data_manager import DataManager

dataManager=DataManager()
def main():
    init_menu()
    pass

def init_menu():
    while True:
        print("1. Print current data"
              "\n2. New Data"
              "\n3. Check Vertex"
              "\n4. Get Dijkstra"
              "\n5. Get BFS"
              "\n6. Exit"
              "\n")

        try:
            ur_select = int(input("Choose an option: "))
        except:
            continue

        if ur_select == 1:
            for key, val in dataManager.data.items():
                print(key + ":{")
                for k, v in val.items():
                    print(k + ": " + str(v[0]) + ", " + str(v[1]))
                print("}")

        elif ur_select == 2:
            setData()

        elif ur_select == 3:
            vertex = input("Please enter the name of the vertex: ")
            print(dataManager.data.get(vertex, "Invalid vertex"))

        elif ur_select == 4:
            setNodes()
            dataManager.setMode("dijkstra")
            print(dataManager.getPath())

        elif ur_select == 5:
            setNodes()
            dataManager.setMode("BFS")
            print(dataManager.getPath())

        elif ur_select == 6:
            quit()

        else:
            print("Invalid input! Enter 1–6.")

def setNodes():
    start = input("Please enter the start node: ")
    end = input("Please enter the end node: ")
    if start in dataManager.data and end in dataManager.data:
        dataManager.setSource(start)
        dataManager.setEnd(end)
    else:
        print("Invalid vertex(s)")
def setData():
    inputType = str(input("Please enter type of input (\"text\" or \"file\" or \"random\"): "))
    if inputType in ["text", "file", "random"]:
        if inputType == "random":
            dataManager.loadData("random", "random")
        elif inputType == "file":
            currInput=input("Please enter filepath: ")
            dataManager.loadData(currInput, inputType)
        elif inputType == "file":
            edges=input("Please enter number of edges: ")
            text=""
            for i in range(edges):
                text += input("Please input an edge (format: N1 N2 0 1): ")
            dataManager.loadData(text, inputType)
    else:
        print("Invalid type")


if __name__ == "__main__":
    main()