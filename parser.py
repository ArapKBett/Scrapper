"""Parse availability and seatmap data"""
import json
import xml.etree.ElementTree as ET
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class DataParser:
    """Parse XML and JSON responses from Tickets.com"""
    
    @staticmethod
    def parse_availability_json(data):
        """Parse availability endpoint JSON response"""
        logger.info("Parsing availability data...")
        
        results = {
            'seatmap_ids': [],
            'event_info': {},
            'raw_data': data
        }
        
        try:
            # Extract seatmap IDs from various possible locations
            if isinstance(data, dict):
                # Check common locations for seatmap data
                if 'seatmaps' in data:
                    results['seatmap_ids'] = data['seatmaps']
                elif 'seatMapId' in data:
                    results['seatmap_ids'].append(data['seatMapId'])
                elif 'seatMapIds' in data:
                    results['seatmap_ids'] = data['seatMapIds']
                
                # Extract event information
                results['event_info'] = {
                    'event_id': data.get('eventId'),
                    'event_name': data.get('eventName'),
                    'venue': data.get('venue'),
                    'date': data.get('date'),
                }
            
            logger.info(f"Found {len(results['seatmap_ids'])} seatmap IDs")
            return results
            
        except Exception as e:
            logger.error(f"Error parsing availability: {e}")
            return results
    
    @staticmethod
    def parse_seatmap_xml(xml_string):
        """Parse seatmap XML data"""
        logger.info("Parsing seatmap XML...")
        
        seats = []
        
        try:
            root = ET.fromstring(xml_string)
            
            # Parse seat elements
            for seat in root.findall('.//seat'):
                seat_data = {
                    'id': seat.get('id'),
                    'section': seat.get('section'),
                    'row': seat.get('row'),
                    'seat_number': seat.get('number'),
                    'price': seat.get('price'),
                    'status': seat.get('status'),
                    'available': seat.get('status') == 'available',
                }
                seats.append(seat_data)
            
            logger.info(f"Parsed {len(seats)} seats from XML")
            return seats
            
        except Exception as e:
            logger.error(f"Error parsing XML: {e}")
            return []
    
    @staticmethod
    def parse_seatmap_json(data):
        """Parse seatmap JSON data"""
        logger.info("Parsing seatmap JSON...")
        
        seats = []
        
        try:
            if isinstance(data, dict):
                # Handle different JSON structures
                seat_data = data.get('seats', []) or data.get('inventory', [])
                
                for seat in seat_data:
                    seat_info = {
                        'id': seat.get('id') or seat.get('seatId'),
                        'section': seat.get('section'),
                        'row': seat.get('row'),
                        'seat_number': seat.get('seatNumber') or seat.get('number'),
                        'price': seat.get('price') or seat.get('amount'),
                        'available': seat.get('available', True),
                        'status': seat.get('status', 'unknown'),
                    }
                    seats.append(seat_info)
            
            logger.info(f"Parsed {len(seats)} seats from JSON")
            return seats
            
        except Exception as e:
            logger.error(f"Error parsing JSON: {e}")
            return []
    
    @staticmethod
    def summarize_availability(seats: List[Dict]) -> Dict:
        """Create summary of availability data"""
        available_seats = [s for s in seats if s.get('available')]
        
        # Group by price
        price_groups = {}
        for seat in available_seats:
            price = seat.get('price', 'Unknown')
            if price not in price_groups:
                price_groups[price] = []
            price_groups[price].append(seat)
        
        summary = {
            'total_seats': len(seats),
            'available_seats': len(available_seats),
            'unavailable_seats': len(seats) - len(available_seats),
            'price_ranges': [],
            'sections': {}
        }
        
        # Price ranges
        for price, price_seats in price_groups.items():
            summary['price_ranges'].append({
                'price': price,
                'count': len(price_seats)
            })
        
        # Section breakdown
        for seat in available_seats:
            section = seat.get('section', 'Unknown')
            if section not in summary['sections']:
                summary['sections'][section] = 0
            summary['sections'][section] += 1
        
        return summary