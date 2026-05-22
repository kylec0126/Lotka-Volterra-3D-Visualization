from paraview.simple import *

# Start fresh
ResetSession()

# 1. GENERATE DATA
math_logic = """
import vtk
opt = self.GetOutput()
pts = vtk.vtkPoints()
t_arr = vtk.vtkFloatArray()
t_arr.SetName("Time")
opt.Allocate(5, 1)
a, b, d, g = 1.1, 0.4, 0.1, 0.4
dt, steps = 0.05, 1000
for start_prey in [5, 10, 15, 20, 25]:
    x, y = float(start_prey), 5.0
    line = vtk.vtkIdList()
    for i in range(steps):
        t = i * dt
        x += (a*x - b*x*y) * dt
        y += (d*x*y - g*y) * dt
        pid = pts.InsertNextPoint(x, y, t)
        line.InsertNextId(pid)
        t_arr.InsertNextValue(t)
    opt.InsertNextCell(vtk.VTK_POLY_LINE, line)
opt.SetPoints(pts)
opt.GetPointData().AddArray(t_arr)
"""

# 2. SOURCE
src = ProgrammableSource(Script=math_logic)
src.OutputDataSetType = 'vtkPolyData'
UpdatePipeline()

# 3. TUBES (Fixed naming for 6.1)
tube = Tube(Input=src)
tube.Radius = 0.3
tube.NumberofSides = 30 
UpdatePipeline()

# 4. VIEW & BACKGROUND (Fixed naming for 6.1)
view = GetActiveViewOrCreate('RenderView')
view.Background = [0.05, 0.05, 0.05]
view.Background2 = [0, 0, 0]
view.BackgroundColorMode = 'Gradient' 

# 5. COLORING (Bulletproof Preset logic)
disp = Show(tube, view)
ColorBy(disp, ('POINTS', 'Time'))
lut = GetColorTransferFunction('Time')

# Try three different names just in case
try:
    lut.ApplyPreset('Viridis', True)
except:
    try:
        lut.ApplyPreset('Inferno', True)
    except:
        lut.ApplyPreset('Cool to Warm', True)

disp.SetScalarBarVisibility(view, True)

# 6. AXES
disp.DataAxesGrid.GridAxesVisibility = 1
disp.DataAxesGrid.XTitle = 'Prey'
disp.DataAxesGrid.YTitle = 'Predator'
disp.DataAxesGrid.ZTitle = 'Time'

Render()
ResetCamera()
print("FINISH: The simulation is ready!")
