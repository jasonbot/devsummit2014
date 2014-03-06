// pythoncppdll.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"

extern "C"
{
  __declspec(dllexport) int AddAreaFieldToFeatureClassCPlusPlus(const wchar_t* feature_class,
                                                                const wchar_t* field_name,
                                                                const void(*callback_function)(int))
  {
    // Convert wchar_t*s to bstring
    _bstr_t catalogPath(feature_class),
            newfieldname(field_name);

    // Coinitialize GP utilities class
    IGPUtilitiesPtr ipUtil(CLSID_GPUtilities);

    // Feature class holder
    IFeatureClassPtr ipFeatureclass(0);

    HRESULT hr;

    // Try to fetch feature class from catalog path
    if (FAILED(hr = ipUtil->OpenFeatureClassFromString(catalogPath, &ipFeatureclass)))
    {
      return -1;
    }

    // Field index of the field of interest
    long fieldIndex;
    if (FAILED(ipFeatureclass->FindField(newfieldname, &fieldIndex)))
    {
      return -2;
    }

    // Set up query and filter
    IQueryFilterPtr ipFilter(CLSID_QueryFilter);
    IFeatureCursorPtr ipCursor;
    IFeaturePtr ipRow;
    IGeometryPtr ipShape;

    // Attempt to set up an edit session
    // if the feature class' workspace type supports it
    IDatasetPtr ipDS(ipFeatureclass);
    IWorkspaceEditPtr ipEditWorkspace;
    if (ipDS)
    {
      IWorkspacePtr ipWorkspace;
      ipDS->get_Workspace(&ipWorkspace);
      ipEditWorkspace = ipWorkspace;
    }

    if (ipEditWorkspace)
    {
      ipEditWorkspace->StartEditing(VARIANT_TRUE);
      ipEditWorkspace->StartEditOperation();
    }

    // Open cursor on feature class
    ipFeatureclass->Update(ipFilter, VARIANT_FALSE, &ipCursor);

    // Row number
    int rowNumber(0);

    // Variant we're going to reuse for the area value
    VARIANT value;
    ::VariantInit(&value);

    // Iterate
    esriGeometryType gt;
    for (ipCursor->NextFeature(&ipRow);
         ipRow != NULL;
         ipCursor->NextFeature(&ipRow))
    {
      // Get row's associated geometry
      ipRow->get_Shape(&ipShape);
      // Ensure we've got a polygon
      ipShape->get_GeometryType(&gt);
      if (gt != esriGeometryPolygon)
      {
        return -3;
      }
      // Get area
      IAreaPtr ipArea(ipShape);
      double area;
      ipArea->get_Area(&area);
      // Pop double into a variant
      value.vt = VT_R8;
      value.dblVal = area;
      // Set double variant onto target field
      ipRow->put_Value(fieldIndex, value);
      // Save
      ipRow->Store();

      if (rowNumber % 100 == 0 && callback_function != NULL)
      {
        callback_function(rowNumber);
      }
      rowNumber++;
    }

    ::VariantClear(&value);

    // Close edit session if pending
    if (ipEditWorkspace)
    {
      ipEditWorkspace->StopEditOperation();
      ipEditWorkspace->StopEditing(VARIANT_TRUE);
    }

    return 0;
  }
}
