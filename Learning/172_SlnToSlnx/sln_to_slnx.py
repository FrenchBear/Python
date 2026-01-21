# slnx.py
# Conversion from old .sln files into modern .slnx files
#
# 2026-01-11    PV

"""
I'd like Python function taking a path as parameter, designed to replace a .sln file (a Visual Studio solution file) with the new format .slnx
This transformation should occur only if the path and all its subfolders only contain one .sln file, one .csproj file and zero .slnx file. If these conditions are not met, a message should be printer and the function returns with no change.
If the conditions are met, a nex .slnx UTF-8 file should be created with following content between lines of dashes:
------------------------
<Solution>
  <Project Path="XXX.csproj" />
</Solution>
------------------------
where XXX.csproj is the name of the unique .csproj file found.
If this .slnx file is successfully written, then rename .sln file using .sln.bak suffix.
"""

from common_fs import get_all_folders
import os

doit = True


def convert_sln_to_slnx(target_directory):
    """
    Scans the directory and subfolders to replace a .sln file with a .slnx file
    only if strict file count conditions are met.
    """
    sln_files = []
    project_files = []
    slnx_files = []

    # Walk the directory tree to count specific file types
    for root, dirs, files in os.walk(target_directory):
        for file in files:
            # Case-insensitive check for extensions
            lower_file = file.lower()
            if lower_file.endswith('.sln'):
                sln_files.append(os.path.join(root, file))
            elif lower_file.endswith('.csproj') or lower_file.endswith('.vbproj'):
                project_files.append(os.path.join(root, file))
            elif lower_file.endswith('.slnx'):
                slnx_files.append(os.path.join(root, file))

    # Check conditions
    # Must have exactly 1 .sln, 1 .csproj, and 0 .slnx
    if len(sln_files) != 1 or len(project_files) != 1 or len(slnx_files) != 0:
        print("Conditions not met for folder", target_directory)
        print(f"Found: {len(sln_files)} .sln files, {len(project_files)} .csproj/.vbproj files, {len(slnx_files)} .slnx files.")
        return

    # Prepare paths and content
    sln_path = sln_files[0]
    csproj_path = project_files[0]
    
    # Get the name of the csproj file (XXX.csproj)
    csproj_name = os.path.basename(csproj_path)
    
    # Determine the path for the new .slnx file 
    # (Same directory and base name as the .sln file)
    sln_dir = os.path.dirname(sln_path)
    sln_filename = os.path.basename(sln_path)
    slnx_filename = os.path.splitext(sln_filename)[0] + ".slnx"
    slnx_full_path = os.path.join(sln_dir, slnx_filename)

    slnx_content = f"""<Solution>
  <Project Path="{csproj_name}" />
</Solution>"""

    # Write new file and rename old one
    if doit:
        try:
            # Write the .slnx file in UTF-8
            with open(slnx_full_path, 'w', encoding='utf-8') as f:
                f.write(slnx_content)
            
            # Rename the original .sln file
            bak_path = sln_path + ".bak"
            if os.path.exists(bak_path):
                os.remove(bak_path)
            os.rename(sln_path, bak_path)
            
            print(f"Success: Created '{slnx_filename}' and renamed original to '{os.path.basename(bak_path)}'.")

        except OSError as e:
            print(f"Error during file operation: {e}")


for rootfile in [
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\001-019\001 VB Elementary\001 VB Elementary.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\001-019\003 VB Anchoring Net6\003 VB Anchoring Net6.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\020-039\029 VB Data\029 VB Data.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\020-039\033 CS ILDASM\033 CS ILDASM.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\020-039\039 CS Deployment\039 CS Deployment.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\040-059\041 VB Enumerator\041 VB Enumerator.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\040-059\042 MCPP IFormattable\042 MCPP IFormattable.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\040-059\044 VB Attributes\044 VB Attributes.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\040-059\046 VB Dim New\046 VB Dim New.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\040-059\050 VB GC sample\050 VB GC sample.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\040-059\052 VB Regular Expressions\052 VB Regular Expressions.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\040-059\054 VB Graphiques\054 VB Graphiques.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\040-059\055 VB Graphiques 2\055 VB Graphiques 2.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\040-059\056 CPP Pentamino Talos\Pentamino 4x4 Talos.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\040-059\056 VB Pentamino\056 VB Pentamino.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\040-059\057 VB Pentamino visuel\057 VB Pentamino visuel.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\040-059\057 VB Pentamino visuel (Old format)\057 VB Pentamino visuel.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\040-059\059 VB ByRef Fields+Inheritance\059 VB ByRef Fields and Inheritance.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\060-079\066 VB Unicode\066 VB Unicode.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\060-079\074 VB Primes plot\074 VB Primes plot.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\060-079\075 VB AfficheImage 2.3\075 VB AfficheImage 2.3.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\060-079\078 VB PicReisze (English)\078 VB PicReisze (English).sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\060-079\078 VB RetailleImages 2.3\078 RetailleImages.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\060-079\078 VB Vignettes\078 VB Vignettes.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\080-099\080 VB Create Tiff Multipage\080 VB Create Tiff Multipage.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\080-099\080 VB ShowTiff Multipage\080 VB ShowTiff Multipage.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\080-099\083 CS String.Format\083 CS String.Format.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\080-099\084 VB LogoEtiq\084 VB LogoEtiq.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\080-099\085 VB StringWidth\085 VB StringWidth.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\080-099\086 VB ImgTo1Bit\086 VB ImgTo1Bit.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\080-099\087 CS DataGrid\087 CS DataGrid.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\080-099\089 VB LVSystem\089 VB LVSystem.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\080-099\090 VB Tests Scripting\090 VB Tests Scripting.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\080-099\091 VB Test CodeDom\091 VB Test CodeDom.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\080-099\093 CS Path\093 CS Path.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\080-099\095 VB MultiThread\095 VB MultiThread.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\080-099\096 VB Radoteur\096 VB Radoteur.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\080-099\097 VB Sort Comics, Rename dir\097 VB Sort Comics.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\080-099\099 VB Components Inheritance\099 VB Components Inheritance.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\100 VB DotNet COM Class\100 VB DotNet COM Class.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\101 CS File\101 CS File.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\102a VB AnalyseComputers\102 VB AnalyseComputers.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\102b VB AnalyseUsers\102 VB AnalyseUsers.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\103 VB AutoScroll and ScrollBars\103 VB AutoScroll and ScrollBars.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\104a VB ImageTool\104a VB ImageTool.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\104b VB Essais Design MugShot\104b VB Essais Design MugShot.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\104c VB Test Form Inheritance\104c VB Test Form Inheritance.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\104d VB FileSystemWatch tests\104d VB FileSystemWatch tests.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\201 VB BookXML\201 VB BookXM.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\202 VB AllEvents WinForms Form\202 VB AllEvents WinForms Form.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\203 VB Inherited Events (Chien)\203 VB Inherited Events (Chien).sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\204 VB Partial Class\204 VB Partial Class.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\205 VB Divers Snippets and XSL\205 VB Divers Snippets and XSL.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\206 VB Reference to Exe\206 VB Reference to Exe.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\207 VB Generics\207 VB Generics.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\208 VB PartialClass2\208 VB PartialClass2.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\100-209\209 VB Protected abuse\209 VB Protected abuse.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\210 VB Type Characters\210 VB Type Characters.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\211 VB Operators (Fraction)\211 VB Operators (Fraction).sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\212 VB Call Timing\212 VB Call Timing.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\213 VB Custom Attribute\213 VB Custom Attribute.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\214 VB DotNetDll\214 VB DotNetDll.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\215 VB Illusion\215 VB Illusion.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\216 VB Launchpad 2005\216 VB Launchpad 2005.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\217 VB Layout Forms\217 VB Layout Forms.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\218 VB ToolStripPanel\218 VB ToolStripPanel.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\220 VB Web Browser\220 VB Web Browser.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\221 VB Tray Icon\221 VB Tray Icon.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\222 VB Icons\222 VB Icons.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\223 VB Printing using ShellExecute\223 VB Printing using ShellExecute.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\224 VB FixWordProperties\224 VB FixWordProperties.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\225 VB AutoScroll and ScrollBars\225 VB AutoScroll and ScrollBars.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\226 VB Text Mixer (Harry Potter)\226 VB Text Mixer (Harry Potter).sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\227 VB IcoToBmp\227 VB IcoToBmp.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\228 VB ImageTool\228 VB ImageTool.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\210-229\229 VB IEnumerable Generic\229 VB IEnumerable Generic.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\301-319\301 VB ODBC to SQL Client\301 VB ODBC to SQL Client.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\301-319\302 VB Create DataTable from schema\302 VB Create DataTable from schema.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\301-319\303 VB Test MetaColumn Names\303 VB Test MetaColumn Names.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\301-319\305 VB RotorRouter\305 VB RotorRouter.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\301-319\306 VB AllStatusBarStyles\306 VB AllStatusBarStyles.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\301-319\307 VB ComboDoubleClic\307 VB ComboDoubleClic.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\301-319\308 VB Splitter.Net\308 VB Splitter.Net.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\301-319\310 VB Lambda functions and Select projections\310 VB Lambda functions and Select projections.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\301-319\311 VB Extensions of IEnumerable(Of T)\311 VB Extensions of IEnumerable(Of T).sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\301-319\312 VB IComparable(Of T)\312 VB IComparable(Of T).sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\301-319\313 VB Partial Methods\313 VB Partial Methods.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\301-319\314 VB PowerCollections\314 VB PowerCollections.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\301-319\315 VB Enumerable Class\315 VB Enumerable Class.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\301-319\316 VB Egality\316 VB Egality.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\301-319\318 VB Linq to Objects\318 VB Linq to Objects.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\301-319\319 VB ShellExecute\319 VB ShellExecute.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\320-329\320 VB Enumerate ODBC Sources\320 VB Enumerate ODBC Sources.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\320-329\322 VB Cordic\322 VB Cordic.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\320-329\323 VB Process in Linq\323 VB Process in Linq.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\320-329\325 VB WPF Fallout 3 Decrypter\325 VB WPF Fallout 3 Decrypter.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\320-329\327 VB KeepTeraAlive\327 VB KeepTeraAlive.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\320-329\328 VB Partition\328 VB Partition.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\320-329\329 VB Wow64DisableWow64FsRedirection\329 VB Wow64DisableWow64FsRedirection.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\400-419\402 VB Initializers\402 VB Initializers.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\400-419\403 VB Linq for Objects\403 VB Linq for Objects.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\400-419\404 VB Start a DLL\404 VB Start a DLL.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\400-419\407 VB Covariant Interface\407 VB Covariant Interface.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\400-419\408 VB ConversionsWithLocales\408 VB ConversionsWithLocales.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\400-419\409 VB Covariance\409 VB Covariance.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\400-419\410 VB Component Walkthrough\410 VB Component Walkthrough.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\400-419\411 VB Multithread Calculations\411 VB Multithread Calculations.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\400-419\412 VB NumTheory\412 VB NumTheory.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\400-419\413 VB SelectAndCount\413 VB SelectAndCount.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\400-419\414 VB CleanEmuleFilenames\414 VB CleanEmuleFilenames.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\400-419\416 VB Boxing and Rational\416 VB Boxing and Rational.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\400-419\417 VB DupFileSize\417 VB DupFileSize.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\400-419\418 VB Covariance\418 VB Covariance.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\420-428\425 VB Egyptian Fractions\425 VB Egyptian Fractions.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\420-428\425 VB Egyption Fractions Tests\425 VB Egyptian Fractions Tests.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\500-519\509 VB Goldbach\509 VB Goldbach.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\520-549\536 CS DLL Settings and Resources\536 CS DLL Settings and Resources.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\520-549\539 C Order\539 C Order.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\520-549\543 VB Arrays\543 VB Arrays.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\601-639\602 C Visual Studio 2017 Trigraphs\602 C Visual Studio 2017 Trigraphs.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\601-639\609 PY Arith2\609 PY Arith2.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\601-639\619 CS Populate Array\619 CS Populate Array.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\601-639\601 CS,VB Visual Studio 2017 New Features\601 VB\601 VB VS2017.sln",
r"c:\Development\GitHub\Visual-Studio-Projects\Net10\601-639\634 CS CPP Lambda\634 CPP LambdaCPP\634 CPP LambdaCPP.sln",

    # r"C:\Development\GitVSTS\DevForFun\01_Labyrinthe\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\01_Labyrinthe\CS_WPF_Net10",
    # r"C:\Development\GitVSTS\DevForFun\02_Hilbert\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\03_Radoteur\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\04_VietnamesePuzzle\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\05_Percolator\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\06_Generics\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\08_EightQueens\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\10_Permutator\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\11_Primes\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\12_ArithDoubler\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\13_SegmentedSieve\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\14_SieveIterator\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\15_TopoSort\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\16_Formatting\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\17_StringCoding\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\18_ConfigFiles\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\19_Dijkstra\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\20_Lex\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\21_FractionDevelopment\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\22_Pentamino\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\23_Regex\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\24_Parallel\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\25_SQL\CS_Net10",
    # r"C:\Development\GitVSTS\DevForFun\26_RotorRouter\CS_Net10",
    ]:
    root,_ = os.path.split(rootfile)
    print(root)
    convert_sln_to_slnx(root)
    for folder in get_all_folders(root):
        print(folder)
        convert_sln_to_slnx(folder)
