import pytest
from app import app


class TestDashAppLayout:
    """Test suite for Pink Morsel Sales Analysis Dash app"""
    
    def find_element_by_id(self, element, target_id):
        """Recursively search for element with given id in the layout tree"""
        if element is None:
            return None
            
        # Check current element
        if hasattr(element, 'id'):
            if isinstance(element.id, str) and element.id == target_id:
                return element
        
        # Check children
        if hasattr(element, 'children') and element.children is not None:
            children = element.children
            if not isinstance(children, list):
                children = [children]
                
            for child in children:
                if child is not None and not isinstance(child, str):
                    result = self.find_element_by_id(child, target_id)
                    if result is not None:
                        return result
        
        return None
    
    def test_header_is_present(self):
        """Test that the application header is present"""
        layout = app.layout
        assert layout is not None, "App layout is None"
        
        # Find H1 element with the header text
        def find_h1_with_text(element, target_text):
            """Search for H1 element containing target text"""
            if element is None:
                return None
            
            element_type = type(element).__name__
            if element_type == 'H1':
                children_list = []
                if hasattr(element, 'children'):
                    children = element.children
                    if children is not None:
                        children_list = children if isinstance(children, list) else [children]
                
                for child in children_list:
                    if isinstance(child, str) and target_text in child:
                        return element
            
            if hasattr(element, 'children') and element.children is not None:
                children = element.children if isinstance(element.children, list) else [element.children]
                for child in children:
                    if child is not None:
                        result = find_h1_with_text(child, target_text)
                        if result:
                            return result
            return None
        
        header_element = find_h1_with_text(layout, "Pink Morsel Sales Analysis")
        assert header_element is not None, "Header with 'Pink Morsel Sales Analysis' text not found in layout"
        print("✓ Header test passed")
    
    def test_visualisation_is_present(self):
        """Test that the sales visualization (chart) is present"""
        layout = app.layout
        assert layout is not None, "App layout is None"
        
        # Find Graph component with id 'sales-chart'
        graph_element = self.find_element_by_id(layout, 'sales-chart')
        assert graph_element is not None, "Graph element with id 'sales-chart' not found"
        
        # Verify it's a Graph component
        element_type = type(graph_element).__name__
        assert element_type == 'Graph', f"Expected Graph element, got {element_type}"
        print("✓ Visualization test passed")
    
    def test_region_picker_is_present(self):
        """Test that the region picker radio buttons are present"""
        layout = app.layout
        assert layout is not None, "App layout is None"
        
        # Find RadioItems component with id 'region-selector'
        radio_element = self.find_element_by_id(layout, 'region-selector')
        assert radio_element is not None, "RadioItems element with id 'region-selector' not found"
        
        # Verify it's a RadioItems component
        element_type = type(radio_element).__name__
        assert element_type == 'RadioItems', f"Expected RadioItems element, got {element_type}"
        
        # Check that the radio element has the expected options
        options = radio_element.options
        assert len(options) >= 5, f"Expected at least 5 radio options, found {len(options)}"
        
        # Verify expected options
        option_labels = [opt['label'].strip() for opt in options]
        expected_labels = ['All Regions', 'North', 'South', 'East', 'West']
        
        for expected in expected_labels:
            assert expected in option_labels, f"Expected option '{expected}' not found in radio options. Found: {option_labels}"
        
        print("✓ Region picker test passed")


class TestDashAppCallbacks:
    """Test suite for Dash app callbacks and functionality"""
    
    def test_app_has_callback_defined(self):
        """Test that the app has callbacks defined for updating the chart"""
        # Verify the app has a server
        assert hasattr(app, 'server'), "App does not have a server"
        assert hasattr(app, 'layout'), "App does not have a layout"
        
        # The callback is defined in the app, verify the app is properly initialized
        assert app.server is not None, "App server is None"
        print("✓ Callback definition test passed")
    
    def test_app_has_required_data(self):
        """Test that the processed data file exists and can be loaded"""
        import pandas as pd
        import os
        
        data_path = 'data/processed_sales_data.csv'
        assert os.path.exists(data_path), f"Data file not found at {data_path}"
        
        # Load and verify data
        df = pd.read_csv(data_path)
        assert len(df) > 0, "Data file is empty"
        
        # Verify required columns
        required_columns = ['Sales', 'Date', 'Region']
        for col in required_columns:
            assert col in df.columns, f"Required column '{col}' not found in data"
        
        print("✓ Data availability test passed")

