import sys
sys.path.append("/Applications/VisIt.app/Contents/Resources/2.8.0/darwin-x86_64/lib/site-packages")
import os
import visit
import alpha

filesPath = "aztec.llnl.gov:/g/g14/damewood/scratchd/2014_Trilayer/vasp"
visit.Launch(vdir="/Applications/VisIt.app/Contents/Resources/bin/")

# Volume plot
visit.OpenDatabase(os.path.join(filesPath,"CHGCAR_DEN"), 0)
visit.AddPlot("Volume", "charge", 1, 1)
VolumeAtts = visit.VolumeAttributes()
VolumeAtts.useColorVarMin = 1
VolumeAtts.colorVarMin = 0
visit.SetPlotOptions(VolumeAtts)

# Atoms and Bonds
visit.OpenDatabase(os.path.join(filesPath,"POSCAR_FULL"), 0)
visit.AddPlot("Molecule", "element", 1, 0)
MoleculeAtts = visit.MoleculeAttributes()
MoleculeAtts.atomSphereQuality = MoleculeAtts.Super  # Low, Medium, High, Super
MoleculeAtts.bondCylinderQuality = MoleculeAtts.Super  # Low, Medium, High, Super
visit.SetPlotOptions(MoleculeAtts)
visit.AddOperator("CreateBonds", 0)
CreateBondsAtts = visit.CreateBondsAttributes()
CreateBondsAtts.elementVariable = "element"
CreateBondsAtts.atomicNumber1 = (14, 14)
CreateBondsAtts.atomicNumber2 = (14, 31)
CreateBondsAtts.minDist = (0.4, 0.4)
CreateBondsAtts.maxDist = (2.5, 2.5)
visit.SetOperatorOptions(CreateBondsAtts, 0)

# Contours
visit.OpenDatabase(os.path.join(filesPath,"CHGCAR_POL"), 0)
visit.AddPlot("Contour", "charge", 1, 0)
visit.AddOperator("Slice", 0)
ContourAtts = visit.ContourAttributes()
ContourAtts.colorType = ContourAtts.ColorBySingleColor  # ColorBySingleColor, ColorByMultipleColors, ColorByColorTable
ContourAtts.singleColor = (255, 255, 255, 255)
ContourAtts.contourNLevels = 10
ContourAtts.minFlag = 1
ContourAtts.maxFlag = 1
ContourAtts.min = -50
ContourAtts.max = 50
visit.SetPlotOptions(ContourAtts)
SliceAtts = visit.SliceAttributes()
SliceAtts.project2d = 0
SliceAtts.axisType = SliceAtts.YAxis
visit.SetOperatorOptions(SliceAtts, 0)

visit.AddPlot("Contour", "charge", 1, 0)
visit.AddOperator("Slice", 0)
ContourAtts = visit.ContourAttributes()
ContourAtts.colorType = ContourAtts.ColorBySingleColor  # ColorBySingleColor, ColorByMultipleColors, ColorByColorTable
ContourAtts.singleColor = (255, 255, 255, 255)
ContourAtts.contourNLevels = 10
ContourAtts.minFlag = 1
ContourAtts.maxFlag = 1
ContourAtts.min = -50
ContourAtts.max = 50
visit.SetPlotOptions(ContourAtts)
SliceAtts = visit.SliceAttributes()
SliceAtts.project2d = 0
SliceAtts.axisType = SliceAtts.XAxis
visit.SetOperatorOptions(SliceAtts, 0)

# Begin spontaneous state
View3DAtts = visit.View3DAttributes()
View3DAtts.viewNormal = (-0.314552, -0.945583, 0.083244)
View3DAtts.focus = (3.85798, 3.85798, 10.9256)
View3DAtts.viewUp = (0,0,1)
View3DAtts.imageZoom = 0.95
visit.SetView3D(View3DAtts)
# End spontaneous state

# Annotations
AnnotationAtts = visit.AnnotationAttributes()
AnnotationAtts.axes3D.visible = 0
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.databaseInfoFlag = 0
AnnotationAtts.timeInfoFlag = 0
AnnotationAtts.legendInfoFlag = 0
AnnotationAtts.backgroundMode = AnnotationAtts.Solid  # Solid, Gradient, Image, ImageSphere
visit.SetAnnotationAttributes(AnnotationAtts)

visit.DrawPlots()

s=visit.SaveWindowAttributes()
s.format = s.TIFF
s.family = False
s.width = 1024*2
s.height = 1024*2
s.fileName = "Trilayer3D_white"
visit.SetSaveWindowAttributes(s)
visit.SaveWindow()
visit.InvertBackgroundColor()
s.fileName = "Trilayer3D_black"
visit.SetSaveWindowAttributes(s)
visit.SaveWindow()
#
#alpha.makeAlpha("Trilayer3D_white.tif", "Trilayer3D_black.tif").save("Trilayer3D_alpha.tif")

#declare visit_ViewNorm  = <-0.314, -0.9455, 0.0832>;
#declare visit_Focus     = <3.85798, 3.85798, 10.9256>;
#declare visit_Up        = <0, 0, 1>;
#declare visit_ViewAngle = 30;
#declare visit_ParallelScale = 12.2122;