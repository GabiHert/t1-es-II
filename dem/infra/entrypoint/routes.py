from flask import Blueprint, jsonify, request
from application import ExtractionService
import logging

api = Blueprint('api', __name__)
logger = logging.getLogger('dem')

@api.route('/health', methods=['GET'])
def health_check():
    try:
        # Try to make a simple database query
        ExtractionService.get_all_loads()
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "service": "dem"
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "service": "dem",
            "error": str(e)
        }), 500

@api.route('/source/<source>/extractions', methods=['GET'])
def get_extractions(source):
    logger.info(f"Getting extractions for source: {source}")
    try:
        extractions = ExtractionService.get_extractions_by_source(source)
        logger.info(f"Successfully retrieved {len(extractions)} extractions for source: {source}")
        return jsonify([{
            'extraction_id': str(e.extraction_id),
            'source': e.source,
            'created_at': e.created_at.isoformat(),
            'status': e.status
        } for e in extractions])
    except Exception as e:
        logger.error(f"Error getting extractions for source {source}: {str(e)}")
        return jsonify({'error': str(e)}), 400

@api.route('/source/<source>/extractions', methods=['POST'])
def create_extraction(source):
    logger.info(f"Creating new extraction for source: {source}")
    try:
        extraction = ExtractionService.create_extraction(source)
        logger.info(f"Successfully created extraction {extraction.extraction_id} for source: {source}")
        return jsonify({
            'extraction_id': str(extraction.extraction_id),
            'source': extraction.source,
            'created_at': extraction.created_at.isoformat(),
            'status': extraction.status
        }), 201
    except Exception as e:
        logger.error(f"Error creating extraction for source {source}: {str(e)}")
        return jsonify({'error': str(e)}), 400

@api.route('/loads', methods=['POST'])
def create_load():
    logger.info("Creating new load")
    try:
        data = request.get_json()
        service = data.get('service')
        extraction_id = data.get('extraction_id')
        
        if not service or not extraction_id:
            logger.error("Missing required parameters: service or extraction_id")
            return jsonify({'error': 'service and extraction_id are required'}), 400
            
        logger.info(f"Creating load for service: {service}, extraction_id: {extraction_id}")
        load = ExtractionService.create_load(service, extraction_id)
        logger.info(f"Successfully created load {load.load_id}")
        return jsonify({
            'load_id': str(load.load_id),
            'extraction_id': str(load.extraction_id),
            'service': load.service,
            'source': load.source,
            'created_at': load.created_at.isoformat(),
            'status': load.status
        }), 201
    except Exception as e:
        logger.error(f"Error creating load: {str(e)}")
        return jsonify({'error': str(e)}), 400

@api.route('/loads', methods=['GET'])
def get_loads():
    logger.info("Getting all loads")
    try:
        loads = ExtractionService.get_all_loads()
        logger.info(f"Successfully retrieved {len(loads)} loads")
        return jsonify([{
            'load_id': str(l.load_id),
            'extraction_id': str(l.extraction_id),
            'service': l.service,
            'source': l.source,
            'created_at': l.created_at.isoformat(),
            'status': l.status
        } for l in loads])
    except Exception as e:
        logger.error(f"Error getting loads: {str(e)}")
        return jsonify({'error': str(e)}), 400

@api.route('/extractions/<extraction_id>', methods=['POST'])
def reprocess_extraction(extraction_id):
    logger.info(f"Reprocessing extraction: {extraction_id}")
    try:
        load = ExtractionService.reprocess_extraction(extraction_id)
        logger.info(f"Successfully reprocessed extraction {extraction_id}, created load {load.load_id}")
        return jsonify({
            'load_id': str(load.load_id),
            'extraction_id': str(load.extraction_id),
            'service': load.service,
            'source': load.source,
            'created_at': load.created_at.isoformat(),
            'status': load.status
        }), 201
    except Exception as e:
        logger.error(f"Error reprocessing extraction {extraction_id}: {str(e)}")
        return jsonify({'error': str(e)}), 400 